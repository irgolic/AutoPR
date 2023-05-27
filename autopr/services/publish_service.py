import json
import sys
import traceback
from typing import Optional, Union, Any, Type

import pydantic
import requests

from autopr.models.artifacts import Issue

import structlog


class CodeBlock(pydantic.BaseModel):
    """
    A block of text to be shown as a code block in the pull request description.
    """
    heading: str
    code: str
    language: str = "xml"
    default_open: bool = False

    def __str__(self):
        return f"""<details{" open" if self.default_open else ""}>
<summary>{self.heading}</summary>

~~~{self.language}
{self.code}
~~~

</details>"""


class UpdateSection(pydantic.BaseModel):
    """
    A section of the pull request description, used to keep state while publishing updates.
    """
    level: int
    title: str
    updates: list[Union[str, CodeBlock, 'UpdateSection']] = pydantic.Field(default_factory=list)


class PublishService:
    """
    Service for publishing updates to the pull request description.

    To control update sections, call:
    - `start_section` to start a new section
    - `end_section` to end the current section (optionally with results and a new title)
    - `update_section` to update the current section title

    To publish updates to the current section, call:
    - `publish_update` to publish a simple textual update
    - `publish_code_block` to publish text in a triple-backtick-style code block
    """

    def __init__(
        self,
        owner: str,
        repo_name: str,
        head_branch: str,
        base_branch: str,
        issue: Optional[Issue] = None,
        pull_request_number: Optional[int] = None,
        loading_gif_url: str = "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        overwrite_existing: bool = False,
    ):
        self.owner = owner
        self.repo_name = repo_name
        self.head_branch = head_branch
        self.base_branch = base_branch
        self.issue = issue
        self.pr_number = pull_request_number
        self.loading_gif_url = loading_gif_url
        self.overwrite_existing = overwrite_existing

        # GitHub comment length limit is ~262144, not 65536 as stated in the docs
        self.max_comment_length = 260000

        if issue is not None:
            self.title: str = f"Fix #{issue.number}: {issue.title}"
        else:
            self.title: str = "AutoPR"
        self.root_section = UpdateSection(
            level=0,
            title="root",
        )
        self.sections_stack: list[UpdateSection] = [self.root_section]

        self.log = structlog.get_logger(service="publish")

        self._last_code_block: Optional[CodeBlock] = None

        self.error_report_template = """
## Traceback

```
{error}
```
"""
        self.new_error_report_link_template = "https://github.com/irgolic/AutoPR/issues/new?" \
                                              "title={title}&" \
                                              "labels=bug&" \
                                              "body={body}"

    def set_title(self, title: str):
        """
        Set the pull request title and body.
        A description heading will be added to the body.

        Parameters
        ----------
        title: str
            The title of the pull request
        body: str
            The body of the pull request
        """
        if self.pr_number is None:
            self.update()
            if self.pr_number is None:
                raise RuntimeError("Error creating pull request")
        else:
            self._set_title(title)

    def publish_update(
        self,
        text: str,
        section_title: Optional[str] = None,
    ):
        """
        Publish a simple text update to the current section.

        Parameters
        ----------
        text: str
            The text to publish
        section_title: str, optional
            The title that the parent section should be updated to
        """
        self.sections_stack[-1].updates.append(text)
        if section_title:
            if self.sections_stack is self.root_section:
                raise ValueError("Cannot set section title on root section")
            self.sections_stack[-1].title = section_title
        self.log.debug("Publishing update", text=text)
        self.update()

    def publish_code_block(
        self,
        heading: str,
        code: str,
        default_open: bool = False,
        language: str = "xml",
        section_title: Optional[str] = None,
    ):
        """
        Publish a code block as a collapsible child to the current section.

        Parameters
        ----------
        heading: str
            The title of the collapsible
        code: str
            The contents of the collapsible
        default_open: bool, optional
            Whether the collapsible should be open by default
        language: str, optional
            The language of the code (defaults to python)
        section_title: str, optional
            The title that the parent section should be updated to
        """
        block = CodeBlock(
            heading=heading,
            code=code,
            language=language,
            default_open=default_open,
        )
        self._last_code_block = block
        self.sections_stack[-1].updates.append(block)
        if section_title:
            if self.sections_stack is self.root_section:
                raise ValueError("Cannot set section title on root section")
            self.sections_stack[-1].title = section_title
        self.update()

    def start_section(
        self,
        title: str,
    ):
        """
        Start a new section.

        Parameters
        ----------
        title: str
            The title of the new section
        """
        self.log.debug("Starting section", title=title)
        new_section = UpdateSection(
            level=len(self.sections_stack),
            title=title,
        )
        self.sections_stack[-1].updates.append(new_section)  # Add the new section as a child
        self.sections_stack.append(new_section)
        self.update()

    def update_section(self, title: str):
        """
        Update the title of the current section.

        Parameters
        ----------
        title: str
            The new title of the current section
        """
        if len(self.sections_stack) == 1:
            raise ValueError("Cannot set section title on root section")
        self.log.debug("Updating section", title=title)
        self.sections_stack[-1].title = title
        self.update()

    def end_section(
        self,
        title: Optional[str] = None,
    ):
        """
        End the current section.

        Parameters
        ----------
        title: str, optional
            The title that section should be updated to
        result: str, optional
            The result of the section
        """
        if len(self.sections_stack) == 1:
            raise ValueError("Cannot end root section")
        self.log.debug("Ending section", title=title)
        if title:
            self.sections_stack[-1].title = title
        self.sections_stack.pop()

        self.update()

    def _contains_last_code_block(self, parent: UpdateSection) -> bool:
        for section in reversed(parent.updates):
            if isinstance(section, CodeBlock):
                return section is self._last_code_block
            elif isinstance(section, UpdateSection):
                return self._contains_last_code_block(section)
        return False

    def _build_progress_update(self, section: UpdateSection, open_default: bool = False) -> str:
        progress = ""
        # Get list of steps
        updates = []
        for update in section.updates:
            if isinstance(update, UpdateSection):
                # Recursively build updates
                updates += [self._build_progress_update(
                    update,
                    open_default=(
                        self._contains_last_code_block(update) or update is section.updates[-1]
                    ),
                )]
                continue
            if isinstance(update, CodeBlock):
                # If is the last code block
                if self._last_code_block is None or update is self._last_code_block or update is section.updates[-1]:
                    # Clone the block and set default_open to True
                    update = update.copy()
                    update.default_open = True
                updates += [str(update)]
                continue
            updates += [update]

        # Prefix updates with quotation
        updates = '\n\n'.join(updates)
        updates = '\n'.join([f"> {line}" for line in updates.splitlines()])

        # Leave the last section open if we're not finalizing (i.e. if we're still running or errored)
        progress += f"""<details{' open' if open_default else ''}>
<summary>{section.title}</summary>

{updates}
</details>"""

        return progress

    def _build_bodies(self, success: Optional[bool] = None) -> list[str]:
        """
        Builds the body of the pull request, splitting it into multiple bodies if necessary.
        Assumes that the top-level section groups are each small enough to fit within `max_comment_length`.
        """
        bodies = []

        body = ""
        if self.issue is not None:
            # Add Fixes magic word
            body += f"Fixes #{self.issue.number}\n\n"

        # Build status
        body += f"## Status\n\n"
        if success is None:
            body += "This pull request is being autonomously generated by [AutoPR](https://github.com/irgolic/AutoPR)."
        elif not success:
            body += f"This pull request was being autonomously generated by " \
                    f"[AutoPR](https://github.com/irgolic/AutoPR), but it encountered an error."
            if sys.exc_info()[0] is not None:
                body += f"\n\nError:\n\n```\n{traceback.format_exc()}\n```"
            body += f'\n\nPlease <a href="{self._build_issue_template_link()}">open an issue</a> to report this.'
        elif success:
            body += f"This pull request was autonomously generated by [AutoPR](https://github.com/irgolic/AutoPR).\n\n" \
                    f"If there's a problem with this pull request, please " \
                    f"[open an issue]({self._build_issue_template_link()})."

        for section in self.root_section.updates:
            if isinstance(section, UpdateSection):
                progress_update = self._build_progress_update(
                    section,
                    open_default=(
                        not success and
                        (section is self.root_section.updates[-1] or self._contains_last_code_block(section))
                    ),
                )
            else:
                progress_update = str(section)
            if len(body) + len('\n\n' + progress_update) > self.max_comment_length:
                bodies += [body]
                body = f"## Status (continued)\n\n{progress_update}"
            else:
                body += f"\n\n{progress_update}"

        if success is None:
            body += f"\n\n" \
                    f'<img src="{self.loading_gif_url}"' \
                    f' width="200" height="200"/>'
        bodies += [body]
        self.log.debug("Built bodies", bodies=bodies)
        return bodies

    def _build_issue_template_link(self, **kwargs):
        if sys.exc_info()[0] is not None:
            error = traceback.format_exc()
        else:
            error = "No traceback"
        kwargs['error'] = error

        body = self.error_report_template.format(**kwargs)
        if sys.exc_info()[0] is not None:
            title = traceback.format_exception_only(sys.exc_info()[0], sys.exc_info()[1])[0].strip()
        elif self.issue is not None:
            title = f'Error fixing "{self.issue.title}"'
        else:
            title = "Error running AutoPR"

        issue_link = self.new_error_report_link_template.format(
            body=body,
            title=title,
        )
        # Map characters to their URL-encoded equivalents
        encoded_url = issue_link.replace(' ', '%20').replace('\n', '%0A').replace('"', '%22').replace("#", "%23")
        return encoded_url

    def update(self):
        """
        Update the PR body with the current progress.
        """
        bodies = self._build_bodies()
        self._publish_progress(bodies)

    def finalize(self, success: bool):
        """
        Finalize the PR, either successfully or unsuccessfully.
        Will render the final PR description without the loading gif.

        Parameters
        ----------
        success: bool
            Whether the PR was successful or not
        """
        bodies = self._build_bodies(success=success)
        self._publish_progress(bodies, success=success)

    def publish_comment(self, text: str, issue_number: Optional[int] = None) -> Optional[str]:
        if issue_number is None:
            if self.pr_number is None:
                self.update()
                if self.pr_number is None:
                    raise RuntimeError("Error creating pull request")
            issue_number = self.pr_number
        return self._publish_comment(text, issue_number)

    def _publish_comment(self, text: str, issue_number: int) -> Optional[str]:
        """
        Publish a comment to the issue (pull requests are also issues).

        Parameters
        ----------

        text: str
            The text to comment
        issue_number: Optional[int]
            The issue number to comment on. If None, should comment on the PR.
        """
        raise NotImplementedError

    def _set_title(self, title: str):
        """
        Set the title of the pull request.

        Parameters
        ----------

        title: str
            The title to set
        """
        raise NotImplementedError

    def _publish_progress(
        self,
        bodies: list[str],
        success: bool = False,
    ):
        """
        Publish the PR to the provider.

        Parameters
        ----------
        title: str
            The title of the PR
        bodies: list[str]
            The bodies of the PR (split into multiple according to `max_comment_length`)
        success: bool
            Whether generation was successful or not
        """
        raise NotImplementedError


class GitHubPublishService(PublishService):
    """
    Publishes the PR to GitHub.

    Sets it as draft while it's being updated, and removes the draft status when it's finalized.
    Adds a shield linking to the action logs, a "Fixes #{issue_number}" link.

    """

    class PRBodySentinel:
        pass

    def __init__(
        self,
        token: str,
        run_id: str,
        owner: str,
        repo_name: str,
        head_branch: str,
        base_branch: str,
        issue: Optional[Issue] = None,
        pull_request_number: Optional[int] = None,
        loading_gif_url: str = "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        overwrite_existing: bool = False,
    ):
        super().__init__(
            owner=owner,
            repo_name=repo_name,
            head_branch=head_branch,
            base_branch=base_branch,
            issue=issue,
            pull_request_number=pull_request_number,
            loading_gif_url=loading_gif_url,
            overwrite_existing=overwrite_existing,
        )
        self.token = token
        self.run_id = run_id

        self._drafts_supported = True
        self._comment_id = None

        # list of comment IDs, incl. PRBodySentinel to denote the body of the PR
        self._comment_ids: list[Union[str, Type[GitHubPublishService.PRBodySentinel]]] = []

        self.max_char_length = 65536

        self.error_report_template = """
{shield}

AutoPR encountered an error.  
Issue: {issue_link}  
Pull Request: {pr_link}

""" + self.error_report_template

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

    def _get_shield(self, success: Optional[bool] = None):
        action_url = f'https://github.com/{self.owner}/{self.repo_name}/actions/runs/{self.run_id}'
        if success is None:
            shield = f"[![AutoPR Running](https://img.shields.io/badge/AutoPR-running-yellow)]({action_url})"
        elif success:
            shield = f"[![AutoPR Success](https://img.shields.io/badge/AutoPR-success-brightgreen)]({action_url})"
        else:
            shield = f"[![AutoPR Failure](https://img.shields.io/badge/AutoPR-failure-red)]({action_url})"
        return shield

    def _build_issue_template_link(self, **kwargs):
        shield = self._get_shield(success=False)
        kwargs['shield'] = shield
        if self.issue is not None:
            kwargs['issue_link'] = f"https://github.com/{self.owner}/{self.repo_name}/issues/{self.issue.number}"
        else:
            kwargs['issue_link'] = "None"
        if self.pr_number is not None:
            kwargs['pr_link'] = f"https://github.com/{self.owner}/{self.repo_name}/pull/{self.pr_number}"
        else:
            kwargs['pr_link'] = "None"
        return super()._build_issue_template_link(**kwargs)

    def _build_bodies(self, success: Optional[bool] = None):
        bodies = super()._build_bodies(success=success)

        # Make shield
        shield = self._get_shield(success=success)
        bodies[0] = shield + '\n\n' + bodies[0]
        return bodies

    def _set_title(self, title: str):
        self._update_pr_title(self.pr_number, title)

    def _publish_progress(self, bodies: list[str], success: bool = False):
        # If overwrite existing, find the PR number
        if not self.pr_number and self.overwrite_existing:
            self.pr_number = self._find_existing_pr()

        # If PR does not exist yet, create it
        if not self.pr_number:
            self.pr_number = self._create_pr(self.title, bodies, success)
            return

        # Update the comments
        for i, body in enumerate(bodies):
            if i >= len(self._comment_ids):
                comment_id = self.publish_comment(body, self.pr_number)
                if comment_id is None:
                    raise RuntimeError("Failed to publish progress comment")
                self._comment_ids.append(comment_id)
                continue
            comment_id = self._comment_ids[i]
            if comment_id is self.PRBodySentinel:
                self._update_pr_body(self.pr_number, body)
            else:
                self._update_pr_comment(str(comment_id), body)

        # Update draft status
        if self._drafts_supported:
            self._set_pr_draft_status(self.pr_number, not success)

    def _find_existing_pr(self):
        """
        Returns the PR dict of the first open pull request with the same head and base branches
        """

        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/pulls'
        headers = self._get_headers()
        params = {'state': 'open', 'head': f'{self.owner}:{self.head_branch}', 'base': self.base_branch}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            prs = response.json()
            if prs:
                return prs[0]  # Return the first pull request found
        else:
            self.log.error('Failed to get pull requests', response_text=response.text)

        return None

    def _create_pr(self, title: str, bodies: list[str], success: bool) -> int:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/pulls'
        headers = self._get_headers()
        data = {
            'head': self.head_branch,
            'base': self.base_branch,
            'title': title,
            'body': bodies[0],
        }
        if self._drafts_supported:
            data['draft'] = "true" if not success else "false"
        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 201:
            # if draft pull request is not supported
            if self._is_draft_error(response.text):
                del data['draft']
                response = requests.post(url, json=data, headers=headers)
                if response.status_code != 201:
                    self.log.error('Failed to create pull request',
                                   code=response.status_code,
                                   response=response.json(),
                                   headers=response.headers)
                    raise RuntimeError('Failed to create pull request')
            else:
                self.log.error('Failed to create pull request',
                               code=response.status_code,
                               response=response.json(),
                               headers=response.headers)
                raise RuntimeError('Failed to create pull request')

        self.log.debug('Pull request created successfully',
                       headers=response.headers)
        pr_number = response.json()['number']

        self._comment_ids = [self.PRBodySentinel]

        # Add additional bodies as comments
        for body in bodies[1:]:
            id_ = self.publish_comment(body, pr_number)
            if id_ is None:
                raise RuntimeError("Failed to publish progress comment")
            self._comment_ids.append(id_)

        return pr_number

    def _patch_pr(self, pr_number: int, data: dict[str, Any]):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}'
        headers = self._get_headers()
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            self.log.debug('Pull request updated successfully')
            return

        self.log.error('Failed to update pull request',
                       code=response.status_code,
                       response=response.json(),
                       headers=response.headers)

    def _is_draft_error(self, response_text: str):
        response_obj = json.loads(response_text)
        is_draft_error = 'message' in response_obj and \
            'draft pull requests are not supported' in response_obj['message'].lower()
        if is_draft_error:
            self.log.warning("Pull request drafts error on this repo")
            self._drafts_supported = False
        return is_draft_error

    def _get_pull_request_node_id(self, pr_number: int) -> str:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/pulls/{pr_number}'
        headers = self._get_headers()
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['node_id']
        else:
            self.log.error('Failed to get pull request node id',
                           code=response.status_code,
                           response=response.json(),
                           headers=response.headers)
            raise RuntimeError('Failed to get pull request node id')

    def _set_pr_draft_status(self, pr_number: int, is_draft: bool):
        pull_request_node_id = self._get_pull_request_node_id(pr_number)
        # sadly this is only supported by graphQL
        if is_draft:
            graphql_query = '''
                mutation ConvertPullRequestToDraft($pullRequestId: ID!) {
                  convertPullRequestToDraft(input: { pullRequestId: $pullRequestId }) {
                    clientMutationId
                  }
                }
            '''
        else:
            graphql_query = '''
                mutation MarkPullRequestReadyForReview($pullRequestId: ID!) {
                  markPullRequestReadyForReview(input: { pullRequestId: $pullRequestId }) {
                    clientMutationId
                  }
                }
            '''
        headers = self._get_headers() | {
            'Content-Type': 'application/json'
        }

        # Undraft the pull request
        data = {'pullRequestId': pull_request_node_id}
        response = requests.post(
            'https://api.github.com/graphql',
            headers=headers,
            json={'query': graphql_query, 'variables': data}
        )

        if response.status_code == 200:
            self.log.debug('Pull request draft status updated successfully')
            return

        self.log.error('Failed to update pull request draft status',
                       code=response.status_code,
                       response=response.json(),
                       headers=response.headers)
        self._drafts_supported = False

    def _update_pr_body(self, pr_number: int, body: str):
        self._patch_pr(pr_number, {'body': body})

    def _update_pr_title(self, pr_number: int, title: str):
        self._patch_pr(pr_number, {'title': title})

    def _update_pr_comment(self, comment_id: str, body: str):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/issues/comments/{comment_id}'
        headers = self._get_headers()
        response = requests.patch(url, json={'body': body}, headers=headers)

        if response.status_code == 200:
            self.log.debug('Comment updated successfully')
            return

        self.log.error('Failed to update comment',
                       code=response.status_code,
                       response=response.json(),
                       headers=response.headers)

    def _publish_comment(self, text: str, issue_number: int) -> Optional[str]:
        url = f'https://api.github.com/repos/{self.owner}/{self.repo_name}/issues/{issue_number}/comments'
        headers = self._get_headers()
        data = {
            'body': text,
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            self.log.debug('Commented on issue successfully')
            return response.json()['id']

        self.log.error('Failed to comment on issue',
                       code=response.status_code,
                       response=response.json(),
                       headers=response.headers)
        return None


class DummyPublishService(PublishService):
    def __init__(self):
        super().__init__(
            owner='',
            repo_name='',
            head_branch='',
            base_branch='',
        )

    def _publish_progress(self, body: str, success: bool = False):
        pass

    def _set_title(self, title: str):
        pass

    def _publish_comment(self, text: str, issue_number: int) -> Optional[str]:
        pass

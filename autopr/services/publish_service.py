import asyncio
import copy
import json
import sys
import traceback
from typing import Optional, Union, Any, Type

import pydantic
import requests

from autopr.log_config import get_logger
from autopr.models.artifacts import Issue, Message, PullRequest
from autopr.services.platform_service import PlatformService, DummyPlatformService


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

    schedule_updates_async = False

    def __init__(
        self,
        platform_service: PlatformService,
        owner: str,
        repo_name: str,
        base_branch: str,
        head_branch: str,
        issue: Optional[Issue] = None,
        pr_number: Optional[int] = None,
        title: Optional[str] = None,
        loading_gif_url: str = "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        overwrite_existing: bool = False,
        **kwargs,
    ):
        self.platform_service = platform_service
        self.owner = owner
        self.repo_name = repo_name
        self.issue = issue
        self.pr_number = pr_number
        self.base_branch = base_branch
        self.head_branch = head_branch

        self.loading_gif_url = loading_gif_url
        self.overwrite_existing = overwrite_existing

        # GitHub comment length limit is ~262144, not 65536 as stated in the docs
        self.max_comment_length = 200000

        # Root publish service instance is used to perform operations
        self.root_publish_service: Optional[PublishService] = None

        # list of comment IDs, incl. PRBodySentinel to denote the body of the PR
        self._comment_ids: list[Union[str, Type[PlatformService.PRBodySentinel]]] = []

        if title is None:
            if issue is not None:
                self.title: str = f"Fix #{issue.number}: {issue.title}"
            else:
                self.title: str = "AutoPR"
        else:
            self.title: str = title
        self.root_section = UpdateSection(
            level=0,
            title="root",
        )
        self.sections_stack: list[UpdateSection] = [self.root_section]

        self.child_count = 0

        self.log = get_logger(service="publish")

        self._last_code_blocks: dict[PublishService, CodeBlock] = {}
        self._scheduled_update_task: Optional[asyncio.Task[Any]] = None

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

    async def create_child(self, title: str) -> 'PublishService':
        """
        Create another instance of publish service, with its root in the current section.
        """
        await self.start_section(title)
        child = type(self)(**self.__dict__)
        child.root_publish_service = self.root_publish_service or self
        child.root_section = self.root_section
        child.sections_stack = [self.sections_stack[-1]]

        self.child_count += 1

        if "path" in self.log._context:
            log_id = self.log._context["path"] + f".{self.child_count}"
        else:
            log_id = f"{self.child_count}"
        child.log = self.log.bind(path=log_id)

        await self.end_section()
        return child

    async def set_title(self, title: str):
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
        if self.root_publish_service is not None:
            return await self.root_publish_service.set_title(title)
        if self.pr_number is None:
            await self.update(wait=True)
            if self.pr_number is None:
                raise RuntimeError("Error creating pull request")
        else:
            await self.platform_service.set_title(title)

    async def publish_update(
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
        await self.update()

    async def publish_code_block(
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
        if self.root_publish_service is not None:
            self.root_publish_service._last_code_blocks[self] = block
        else:
            self._last_code_blocks[self] = block
        self.sections_stack[-1].updates.append(block)
        if section_title:
            if self.sections_stack is self.root_section:
                raise ValueError("Cannot set section title on root section")
            self.sections_stack[-1].title = section_title
        await self.update()

    async def start_section(
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
        await self.update()

    async def update_section(self, title: str):
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
        await self.update()

    async def end_section(
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

        await self.update()

    async def merge(
        self,
        reason: Optional[str] = None,
    ):
        """
        Merge the pull request.
        """
        if self.root_publish_service is not None:
            return await self.root_publish_service.merge()
        if self.pr_number is None:
            self.log.warning("PR merge requested, but does not exist")
            return
        if reason is not None:
            await self.publish_comment(reason)
        return await self.platform_service.merge_pr(
            self.pr_number,
            commit_title=self.title,
        )

    async def close(
        self,
        reason: Optional[str] = None,
    ):
        """
        Close the pull request.
        """
        if self.root_publish_service is not None:
            return await self.root_publish_service.close()
        if self.pr_number is None:
            self.log.warning("PR close requested, but does not exist")
            return
        if reason is not None:
            await self.publish_comment(reason)
        return await self.platform_service.close_pr(self.pr_number)

    def _contains_last_code_block(self, parent: UpdateSection) -> bool:
        for section in reversed(parent.updates):
            if isinstance(section, CodeBlock):
                return section in self._last_code_blocks.values()
            elif isinstance(section, UpdateSection):
                return self._contains_last_code_block(section)
        return False

    def _build_progress_update(
        self,
        leaf_node_count: int,
        section: UpdateSection,
        open_default: bool = False,
        is_root: bool = False,
    ) -> tuple[str, int]:
        progress = ""
        # Get list of steps
        updates = []
        for update in section.updates:
            if leaf_node_count == 0:
                break

            if isinstance(update, UpdateSection):
                # Recursively build updates
                new_update, leaf_node_count = self._build_progress_update(
                    leaf_node_count,
                    update,
                    open_default=(
                        self._contains_last_code_block(update) or update is section.updates[-1]
                    ),
                )
                updates += [new_update]
                continue

            leaf_node_count -= 1

            if isinstance(update, CodeBlock):
                # If is the last code block
                if update is self._last_code_blocks.values() or update is section.updates[-1]:
                    # Clone the block and set default_open to True
                    update = update.copy()
                    update.default_open = True
                updates += [str(update)]
                continue
            updates += [update]

        # Prefix updates with quotation
        updates_str = '\n\n'.join(updates)

        # Leave the last section open if we're not finalizing (i.e. if we're still running or errored)
        if not is_root:
            if len(updates) > 1:
                updates_str = '\n'.join([f"> {line}" for line in updates_str.splitlines()])
            elif len(updates) == 1 and section.level > 1:
                open_default = True
            progress += f"""<details{' open' if open_default else ''}>
<summary>{section.title}</summary>

{updates_str}
</details>"""
        else:
            progress += updates_str

        return progress, leaf_node_count

    def _pop_leaf_nodes(self, section: UpdateSection, num: int) -> int:
        while num > 0:
            if len(section.updates) == 0:
                break
            elif isinstance(section.updates[0], UpdateSection):
                num = self._pop_leaf_nodes(section.updates[0], num)
                if len(section.updates[0].updates) == 0:
                    section.updates.pop(0)
            else:
                section.updates.pop(0)
                num -= 1
        return num

    def _build_bodies(self, success: Optional[bool] = None, exceptions: Optional[list[Exception]] = None) -> list[str]:
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
            if exceptions:
                for exception in exceptions:
                    body += (f"\n\nError:\n\n```\n"
                             f"{traceback.format_exception(type(exception), exception, exception.__traceback__)}"
                             f"\n```")
            body += f'\n\nPlease <a href="{self._build_issue_template_link()}">open an issue</a> to report this.'
        elif success:
            body += f"This pull request was autonomously generated by [AutoPR](https://github.com/irgolic/AutoPR).\n\n" \
                    f"If there's a problem with this pull request, please " \
                    f"[open an issue]({self._build_issue_template_link()})."

        # Iteratively try adding n sections to the body until we hit the max length
        root = copy.deepcopy(self.root_section)
        n = 0
        while root.updates:
            new_body = body
            finished = False
            while len(new_body) < self.max_comment_length and not finished:
                n += 1
                progress_update, finished = self._build_progress_update(
                    n,
                    root,
                    open_default=(
                        not success
                    ),
                    is_root=True,
                )
                new_body = body + f"\n\n{progress_update}"
            bodies += [new_body]
            self._pop_leaf_nodes(root, n)
            if finished:
                break
            body = f"## Status (continued)"
            n = 0
        if not bodies:
            bodies += [body]

        if success is None:
            bodies[-1] += f"\n\n" \
                          f'<img src="{self.loading_gif_url}"' \
                          f' width="200" height="200"/>'
        # self.log.debug("Built bodies", bodies=bodies)
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

    async def update(self, wait: bool = False):
        """
        Schedule an _update call in the async event loop, at most once every two seconds.
        """
        if self.root_publish_service is not None:
            return await self.root_publish_service.update(wait=wait)
        if not self.schedule_updates_async:
            return await self._update()

        if self._scheduled_update_task is not None:
            # wait for the previous update to finish
            if wait:
                self.log.debug("Waiting for previous update to finish")
                await self._scheduled_update_task
            return
        self.log.debug("Scheduling update")
        self._scheduled_update_task = asyncio.create_task(self._update())
        if wait:
            self.log.debug("Waiting for update to finish")
            await self._scheduled_update_task

    async def _update(self):
        """
        Update the PR body with the current progress.
        """
        try:
            bodies = self._build_bodies()
            await self._publish_progress(bodies)
        except Exception:
            self.log.error("Error updating PR", exc_info=True)
        finally:
            self._scheduled_update_task = None
            self.log.debug("Update finished")

    async def finalize(self, success: bool, exceptions: Optional[list[Exception]] = None):
        """
        Finalize the PR, either successfully or unsuccessfully.
        Will render the final PR description without the loading gif.

        Parameters
        ----------
        success: bool
            Whether the PR was successful or not
        exceptions: Optional[list[Exception]]
            A list of exceptions that occurred during the PR
        """
        bodies = self._build_bodies(success=success)
        await self._publish_progress(bodies, success=success)

    async def publish_comment(self, text: str, issue_number: Optional[int] = None) -> Optional[str]:
        if self.root_publish_service is not None:
            return await self.root_publish_service.publish_comment(text, issue_number)
        if issue_number is None:
            if self.pr_number is None:
                await self.update(wait=True)
                if self.pr_number is None:
                    raise RuntimeError("Error creating pull request")
            issue_number = self.pr_number
        return await self.platform_service.publish_comment(text, issue_number)

    async def _publish_progress(
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
        # If overwrite existing, find the PR number
        if not self.pr_number and self.overwrite_existing:
            pr_number = await self.platform_service.find_existing_pr(self.head_branch, self.base_branch)
            if pr_number is not None:
                self.pr_number = pr_number

        # If PR does not exist yet, create it
        # TODO `pr_number` is not propagated to children!
        #  with lists they retain the reference, but with ints they don't
        if not self.pr_number:
            pr_number, comment_ids = await self.platform_service.create_pr(
                self.title,
                bodies,
                success,
                self.head_branch,
                self.base_branch
            )
            if pr_number is None:
                raise RuntimeError("Failed to create PR")
            self.pr_number = pr_number
            self._comment_ids.extend(comment_ids)
            return

        # Update the comments
        for i, body in enumerate(bodies):
            if i >= len(self._comment_ids):
                comment_id = await self.publish_comment(body, self.pr_number)
                if comment_id is None:
                    raise RuntimeError("Failed to publish progress comment")
                    # self.log.error("Failed to publish progress comment")
                self._comment_ids.append(comment_id)
                continue
            comment_id = self._comment_ids[i]
            if comment_id is PlatformService.PRBodySentinel:
                await self.platform_service.update_pr_body(self.pr_number, body)
            else:
                await self.platform_service.update_comment(str(comment_id), body)

        # Update draft status
        await self.platform_service.set_pr_draft_status(self.pr_number, not success)


class GitHubPublishService(PublishService):
    """
    Publishes the PR to GitHub.

    Sets it as draft while it's being updated, and removes the draft status when it's finalized.
    Adds a shield linking to the action logs, a "Fixes #{issue_number}" link.

    """

    schedule_updates_async = True

    def __init__(
        self,
        platform_service,
        run_id: str,
        owner: str,
        repo_name: str,
        base_branch: str,
        head_branch: str,
        issue: Optional[Issue] = None,
        pr_number: Optional[int] = None,
        title: Optional[str] = None,
        loading_gif_url: str = "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        overwrite_existing: bool = False,
        **kwargs,
    ):
        super().__init__(
            platform_service=platform_service,
            owner=owner,
            repo_name=repo_name,
            issue=issue,
            pr_number=pr_number,
            loading_gif_url=loading_gif_url,
            title=title,
            overwrite_existing=overwrite_existing,
            head_branch=head_branch,
            base_branch=base_branch,
            **kwargs,
        )
        self.run_id = run_id

        self.error_report_template = """
{shield}

AutoPR encountered an error.  
Issue: {issue_link}  
Pull Request: {pr_link}

""" + self.error_report_template

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

    def _build_bodies(self, success: Optional[bool] = None, exceptions: Optional[list[Exception]] = None):
        bodies = super()._build_bodies(success=success, exceptions=exceptions)

        # Make shield
        shield = self._get_shield(success=success)
        bodies[0] = shield + '\n\n' + bodies[0]
        return bodies


class DummyPublishService(PublishService):
    def __init__(self, *args, **kwargs):
        super().__init__(
            platform_service=DummyPlatformService(),
            owner='',
            repo_name='',
            base_branch='',
            head_branch='',
        )

    async def start_section(
        self,
        title: str,
    ):
        print(f'Start section: {title}')

    async def end_section(
        self,
        title: Optional[str] = None,
    ):
        print('End section')

    async def publish_update(
        self,
        text: str,
        section_title: Optional[str] = None,
    ):
        print(text)

    async def publish_code_block(
        self,
        heading: str,
        code: str,
        default_open: bool = False,
        language: str = "xml",
        section_title: Optional[str] = None,
    ):
        print(f"""
{heading}
```{language}        
{code}
```""")

    async def finalize(self, success: bool, exceptions: Optional[list[Exception]] = None):
        pass

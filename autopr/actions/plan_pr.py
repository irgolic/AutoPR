from autopr.actions.base import Action, ContextDict
from autopr.actions.utils.commit import PullRequestDescription
from autopr.models.artifacts import Issue
from autopr.models.prompt_rails import PromptRail


class ProposePullRequestRail(PromptRail):
    # Generate proposed list of commit messages, given notes and issue
    prompt_template = f"""Hey somebody just submitted an issue, could you own it, write some commits, and a pull request?

These are notes we took while looking at the repo:
```{{notes_taken_while_looking_at_files}}```

This is the issue that was opened:
```{{issue}}```

When you're done, send me the pull request title, body, and a list of commits, each coupled with which files we should be looking at to write the commit's code.
Ensure you specify the files relevant to the commit, especially if the commit is a refactor.
Folders are created automatically; do not make them in their own commit."""

    output_type = PullRequestDescription
    # extra_params = {
    #     'temperature': 0.1,
    # }

    notes_taken_while_looking_at_files: str
    issue: Issue


class PlanPullRequest(Action):
    id = "plan_pull_request"
    description = "Propose a pull request to the user."

    def propose_pull_request(self, issue: Issue, notes: str) -> PullRequestDescription:
        self.log.debug('Getting commit messages...')
        pr_desc = self.rail_service.run_prompt_rail(
            ProposePullRequestRail(
                issue=issue,
                notes_taken_while_looking_at_files=notes,
            )
        )
        if pr_desc is None or not isinstance(pr_desc, PullRequestDescription):
            raise ValueError('Error proposing pull request')
        return pr_desc

    def run(
        self,
        args: Action.Arguments,
        context: ContextDict,
    ) -> ContextDict:
        self.publish_service.update_section('📝 Planning pull request')
        # Get issue
        if 'issue' not in context:
            raise ValueError('No `issue` key in context')
        issue = context['issue']
        if not isinstance(issue, Issue):
            raise ValueError(f'Context `issue` is type {type(issue)}, not Issue')

        # Get notes
        if 'notes' not in context:
            raise ValueError('No `notes` key in context')
        notes = context['notes']
        if not isinstance(notes, str):
            raise ValueError(f'Context `notes` is type {type(notes)}, not str')

        # Write pull request description
        pr_desc = self.propose_pull_request(issue, notes)

        # Save the pull request description to the context
        context['pull_request_description'] = pr_desc

        self.publish_service.update_section('📝 Planned pull request')
        return context

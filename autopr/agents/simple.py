from typing import Collection

import structlog

from autopr.actions.base import ContextDict
from autopr.actions.utils.commit import PullRequestDescription
from autopr.agents.base import Agent
from autopr.models.events import EventUnion

log = structlog.get_logger()


class Simple(Agent):
    """
    A simple Brain agent that:
    - Plans a pull request
    - Implements each commit in the pull request
    """

    #: The ID of the agent, used to identify it in the settings
    id = "simple"

    def __init__(
        self,
        *args,
        plan_pull_request_action: str = "plan_pull_request",
        codegen_actions: Collection[str] = (
            'new_file',
            'edit_file',
        ),
        max_codegen_iterations: int = 5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.plan_pull_request_action = plan_pull_request_action
        self.codegen_actions = codegen_actions
        self.max_codegen_iterations = max_codegen_iterations

    def handle_event(
        self,
        event: EventUnion,
    ) -> None:
        issue = event.issue

        # Initialize the context
        context = ContextDict(
            issue=issue,
        )

        # Generate the pull request plan (commit messages and relevant filepaths)
        context = self.action_service.run_action(self.plan_pull_request_action, context)

        # Get the pull request description from the context
        if 'pull_request_description' not in context:
            raise ValueError(f"Action {self.plan_pull_request_action} did not return a pull request description")
        pr_desc = context['pull_request_description']
        if not isinstance(pr_desc, PullRequestDescription):
            raise TypeError(f"Action {self.plan_pull_request_action} returned a pull request description of type "
                            f"{type(pr_desc)} instead of PullRequestDescription")

        # Publish the description
        self.publish_service.set_pr_description(pr_desc.title, pr_desc.body)

        for current_commit in pr_desc.commits:
            self.publish_service.start_section(f"🔨 Writing commit {current_commit.commit_message}")

            # Generate the changes
            context = self.action_service.run_actions_iteratively(
                self.codegen_actions,
                context,
                max_iterations=self.max_codegen_iterations,
            )

            # Commit and push the changes
            self.commit_service.commit(current_commit.commit_message, push=True)

            if self.diff_service.get_diff():
                self.publish_service.end_section(f"✅ Committed {current_commit.commit_message}")
            else:
                self.publish_service.end_section(f"⚠️ Empty commit {current_commit.commit_message}")

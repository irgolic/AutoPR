from typing import Collection

import structlog

from autopr.actions.base import ContextDict
from autopr.actions.utils.commit import PullRequestDescription, CommitPlan, PullRequestAmendment
from autopr.agents.base import Agent
from autopr.models.events import EventUnion, PullRequestCommentEvent, IssueLabelEvent

log = structlog.get_logger()


class PlanAndCode(Agent):
    """
    A simple agent that:
    - plans commits from issues or pull request comments,
    - opens and responds to pull requests,
    - writes commits to the pull request.
    """

    #: The ID of the agent, used to identify it in the settings
    id = "plan_and_code"

    def __init__(
        self,
        *args,
        inspection_actions: Collection[str] = (
            "look_at_files",
        ),
        planning_actions: Collection[str] = (
            "plan_pull_request",
            "request_more_information"
        ),
        response_actions: Collection[str] = (
            "plan_commits",
            "request_more_information",
        ),
        codegen_actions: Collection[str] = (
            'new_file',
            'edit_file',
        ),
        max_codegen_iterations: int = 5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.inspection_actions = inspection_actions
        self.planning_actions = planning_actions
        self.response_actions = response_actions
        self.codegen_actions = codegen_actions
        self.max_codegen_iterations = max_codegen_iterations

    def write_commit(
        self,
        commit_plan: CommitPlan,
        context: ContextDict,
        context_headings: dict[str, str]
    ) -> ContextDict:
        self.publish_service.start_section(f"🔨 Writing commit {commit_plan.commit_message}")

        # Set the current commit in the context
        context['current_commit'] = commit_plan

        # Clear action_history in the context for each commit
        context['action_history'] = []

        # Generate the changes
        context = self.action_service.run_actions_iteratively(
            self.codegen_actions,
            context,
            context_headings={
                'current_commit': f'Commit we are currently generating: {commit_plan.commit_message}',
                'action_history': 'Actions that have been run so far',
                **context_headings,
            },
            max_iterations=self.max_codegen_iterations,
            include_finished=True,
        )

        # Show the diff in the progress report
        diff = self.diff_service.get_diff()
        if diff:
            self.publish_service.publish_code_block(
                heading="Diff",
                code=diff,
                language="diff",
            )
            self.publish_service.end_section(f"✅ Committed {commit_plan.commit_message}")
        else:
            self.publish_service.end_section(f"⚠️ Empty commit {commit_plan.commit_message}")

        # Commit and push the changes
        self.commit_service.commit(commit_plan.commit_message, push=True)

        return context

    def respond_to_pr_comment(
        self,
        event: PullRequestCommentEvent,
    ):
        # Checkout the head branch
        head_branch = event.pull_request.head_branch
        base_branch = event.pull_request.base_branch
        self.repo.heads[head_branch].checkout()

        # Get list of commits on the branch
        commits = [
            commit.message
            for commit in self.repo.iter_commits(f"origin/{base_branch}..{head_branch}")
        ]

        # Initialize the context
        context = ContextDict(
            commits_in_pull_request=commits,
            request=event.new_comment,
        )

        # Run the inspection actions
        context = self.action_service.run_actions_iteratively(
            self.inspection_actions,
            context,
            max_iterations=1,
        )

        # Run the response actions
        context = self.action_service.run_actions_iteratively(
            self.response_actions,
            context,
            max_iterations=1,
        )

        # Get the pull request description from the context
        if 'pull_request_amendment' not in context:
            # Stop the agent if the action did not return a pull request description
            return
        pull_request_amendment = context['pull_request_amendment']
        if not isinstance(pull_request_amendment, PullRequestAmendment):
            raise ValueError(f"Action returned a pull request amendment that is not a PullRequestDescription object")

        if pull_request_amendment.comment:
            # Comment on the pull request
            self.publish_service.publish_comment(pull_request_amendment.comment)

        if pull_request_amendment.commits:
            # Stop the agent if the action did not return a pull request description
            commits = pull_request_amendment.commits
            if not all(isinstance(commit, CommitPlan)
                       for commit in commits):
                raise ValueError(f"Action returned commits that are not CommitPlan objects")

            for current_commit in commits:
                context = self.write_commit(
                    current_commit,
                    context,
                    context_headings={
                        'pull_request': "Pull request that we are adding commits to",
                        'request': "Request that we are responding to",
                    }
                )
                self.log.info(f"Committed {current_commit.commit_message}")

    def create_pull_request(
        self,
        event: IssueLabelEvent,
    ) -> None:
        # Create new branch
        self.commit_service.overwrite_new_branch()

        issue = event.issue

        # Initialize the context
        context = ContextDict(
            issue=issue,
        )

        # Run the inspection actions
        context = self.action_service.run_actions_iteratively(
            self.inspection_actions,
            context,
            max_iterations=1,
        )

        # Generate the pull request plan (commit messages and relevant filepaths)
        context = self.action_service.run_actions_iteratively(
            self.planning_actions,
            context,
            max_iterations=1,
        )

        # Get the pull request description from the context
        if 'pull_request_description' not in context:
            # Stop the agent if the action did not return a pull request description
            return
        pr_desc = context['pull_request_description']
        if not isinstance(pr_desc, PullRequestDescription):
            raise TypeError(f"Actions returned a pull request description of type "
                            f"{type(pr_desc)} instead of PullRequestDescription")

        # Publish the description
        self.publish_service.set_title(pr_desc.title)
        self.publish_service.publish_comment(pr_desc.body)

        for current_commit in pr_desc.commits:
            context = self.write_commit(
                current_commit,
                context,
                context_headings={
                    'pull_request_description': 'Plan for the pull request',
                },
            )

    def handle_event(
        self,
        event: EventUnion,
    ) -> None:
        if isinstance(event, IssueLabelEvent):
            self.create_pull_request(event)
        elif isinstance(event, PullRequestCommentEvent):
            self.respond_to_pr_comment(event)
        else:
            raise NotImplementedError(f"Event type {type(event)} not supported")

from typing import Collection

import structlog

from autopr.actions.base import ContextDict
from autopr.actions.utils.commit import PullRequestDescription, CommitPlan, PullRequestAmendment
from autopr.agents.base import Agent
from autopr.models.events import EventUnion, PullRequestCommentEvent, IssueLabelEvent

log = structlog.get_logger()

class PlanAndCode(Agent):
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

        commit_index = context.get("commits_in_pull_request", []).index(commit_plan.commit_message) + 1
        context_headings['current_commit'] = f"Commit {commit_index}/{len(context['commits_in_pull_request'])}: {commit_plan.commit_message}"
        context['current_commit'] = commit_plan
        context['action_history'] = []

        context = self.action_service.run_actions_iteratively(
            self.codegen_actions,
            context,
            context_headings={
                'current_commit': context_headings['current_commit'],
                'action_history': 'Actions that have been run so far',
                **context_headings,
            },
            max_iterations=self.max_codegen_iterations,
            include_finished=True,
        )

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

        self.commit_service.commit(commit_plan.commit_message, push=True)

        return context
from typing import Union

from git.repo import Repo

from autopr.models.artifacts import Issue
from .base import BrainAgentBase

import structlog

from ...models.events import EventUnion

log = structlog.get_logger()


class BasicBrainAgent(BrainAgentBase):
    def _generate_pr(
        self,
        event: EventUnion,
    ) -> None:
        issue = event.issue

        # Switch to the base branch
        self.commit_service.overwrite_new_branch()

        # Get the commit messages and relevant filepaths
        pr_desc = self.pull_request_agent.plan_pull_request(self.repo, issue, event)

        is_published = False
        for current_commit in pr_desc.commits:
            # Generate the changes
            self.codegen_agent.generate_changes(
                self.repo,
                issue,
                pr_desc,
                current_commit
            )

            # Commit the changes
            self.commit_service.commit(current_commit)

            # Publish the PR after the first commit is written
            if not is_published:
                self.publish_service.publish(pr_desc)
                is_published = True

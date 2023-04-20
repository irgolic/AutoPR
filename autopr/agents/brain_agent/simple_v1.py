from .base import BrainAgentBase

import structlog

from ...models.events import EventUnion

log = structlog.get_logger()


class BasicBrainAgent(BrainAgentBase):
    id = "simple-v1"

    def _generate_pr(
        self,
        event: EventUnion,
    ) -> None:
        issue = event.issue

        # Get the commit messages and relevant filepaths
        pr_desc = self.pull_request_agent.plan_pull_request(self.repo, issue, event)

        # Publish the description
        self.publish_service.set_pr_description(pr_desc)

        for current_commit in pr_desc.commits:
            # Generate the changes
            self.codegen_agent.generate_changes(
                self.repo,
                issue,
                pr_desc,
                current_commit
            )

            # Commit and push the changes
            self.commit_service.commit(current_commit, push=True)

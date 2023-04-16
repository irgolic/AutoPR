from typing import Union

from git.repo import Repo

from autopr.models.artifacts import Issue
from .commit_service import CommitService
from .publish_service import PublishService
from .rail_service import RailService
from ..agents.codegen_agent import CodegenAgent
from ..agents.pull_request_agent import PullRequestAgent

import structlog

from ..models.events import EventUnion

log = structlog.get_logger()


class GenerationService:
    def __init__(
        self,
        codegen_agent: CodegenAgent,
        pull_request_agent: PullRequestAgent,
        rail_service: RailService,
        commit_service: CommitService,
        publish_service: PublishService,
    ):
        self.codegen_agent = codegen_agent
        self.pull_request_agent = pull_request_agent
        self.rail_service = rail_service
        self.commit_service = commit_service
        self.publish_service = publish_service

    def generate_pr(
        self,
        repo: Repo,
        issue: Issue,
        event: EventUnion,
    ) -> None:
        # Switch to the base branch
        self.commit_service.overwrite_new_branch()

        # Get the commit messages and relevant filepaths
        pr_desc = self.pull_request_agent.plan_pull_request(repo, issue, event)

        is_published = False
        for current_commit in pr_desc.commits:
            # Generate the changes
            self.codegen_agent.generate_changes(
                repo,
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

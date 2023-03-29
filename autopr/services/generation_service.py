import tempfile
from typing import Callable, Union

from git.repo import Repo
import pydantic
import transformers
from git import Tree

from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \
    Diff, CommitPlan
from autopr.models.prompt_rails import InitialFileSelect, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \
    NewDiff, FileDescriptor
from .commit_service import CommitService
from .publish_service import PublishService
from .rail_service import RailService
from ..agents.codegen_agent import CodegenAgent
from ..agents.pull_request_agent import PullRequestAgent

import structlog

from ..models.events import IssueCommentEvent, IssueOpenedEvent

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
        event: Union[IssueOpenedEvent, IssueCommentEvent]
    ) -> None:
        # Switch to the base branch
        self.commit_service.overwrite_new_branch()

        # Get the commit messages and relevant filepaths
        pr_desc = self.pull_request_agent.plan_pull_request(repo, issue, event)

        is_published = False
        for current_commit in pr_desc.commits:
            # Generate the patch
            diff = self.codegen_agent.generate_patch(
                repo,
                issue,
                pr_desc,
                current_commit
            )

            # Apply the patch and commit the changes
            self.commit_service.commit(current_commit, diff)

            # Publish the PR after the first commit is written
            if not is_published:
                self.publish_service.publish(pr_desc)
                is_published = True

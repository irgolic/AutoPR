import tempfile
from typing import Callable

from git.repo import Repo
import pydantic
import transformers
from git import Tree

from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \
    Diff, CommitPlan
from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \
    NewDiff, FileDescriptor
from autopr.services.codegen_service import CodegenService
from autopr.services.commit_service import CommitService
from autopr.services.planner_service import PlannerService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService

import structlog
log = structlog.get_logger()


class GenerationService:
    def __init__(
        self,
        codegen_service: CodegenService,
        planner_service: PlannerService,
        rail_service: RailService,
        commit_service: CommitService,
        publish_service: PublishService,
    ):
        self.codegen_service = codegen_service
        self.planner_service = planner_service
        self.rail_service = rail_service
        self.commit_service = commit_service
        self.publish_service = publish_service

    def generate_pr(
        self,
        repo: Repo,
        issue: Issue,
    ) -> None:
        # Switch to the base branch
        self.commit_service.overwrite_new_branch()

        # Get the commit messages and relevant filepaths
        pr_desc = self.planner_service.plan_pr(repo, issue)

        is_published = False
        for current_commit in pr_desc.commits:
            # Generate the patch
            diff = self.codegen_service.generate_patch(
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

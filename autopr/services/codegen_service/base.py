from typing import ClassVar

from git.repo import Repo

from autopr.models.artifacts import DiffStr, Issue
from autopr.models.rail_objects import PullRequestDescription, CommitPlan
from autopr.models.rails import FileDescriptor
from autopr.services.diff_service import DiffService
from autopr.services.rail_service import RailService

import structlog


class CodegenServiceBase:
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        diff_service: DiffService,
        repo: Repo,
        **kwargs,
    ):
        self.rail_service = rail_service
        self.diff_service = diff_service
        self.repo = repo

        self.log = structlog.get_logger(service="codegen",
                                        id=self.id)
        if kwargs:
            self.log.warning("Codegen did not use additional options", kwargs=kwargs)

    def generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> DiffStr:
        self.log.info("Generating patch", issue=issue)
        patch = self._generate_patch(repo, issue, pr_desc, current_commit)
        self.log.info("Generated patch", issue=issue, patch=patch)
        return patch

    def _generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> DiffStr:
        raise NotImplementedError

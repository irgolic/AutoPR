from typing import ClassVar

from git.repo import Repo

from autopr.models.artifacts import DiffStr, Issue
from autopr.models.rail_objects import PullRequestDescription, CommitPlan
from autopr.services.chain_service import ChainService
from autopr.services.diff_service import DiffService
from autopr.services.rail_service import RailService

import structlog


class CodegenAgentBase:
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        chain_service: ChainService,
        diff_service: DiffService,
        repo: Repo,
        **kwargs,
    ):
        self.rail_service = rail_service
        self.chain_service = chain_service
        self.diff_service = diff_service
        self.repo = repo

        self.log = structlog.get_logger(service="codegen",
                                        id=self.id)
        if kwargs:
            self.log.warning("Codegen did not use additional options", kwargs=kwargs)

    def generate_changes(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> None:
        self.log.info("Generating changes", issue=issue)
        self._generate_changes(repo, issue, pr_desc, current_commit)
        self.log.info("Generated changes", issue=issue)

    def _generate_changes(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> None:
        raise NotImplementedError

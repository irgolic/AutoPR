from typing import ClassVar

from git.repo import Repo

from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription
from autopr.models.rails import FileDescriptor
from autopr.services.rail_service import RailService

import structlog


class PlannerServiceBase:
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        **kwargs,
    ):
        self.rail_service = rail_service

        self.log = structlog.get_logger(service="planner",
                                        id=self.id)
        if kwargs:
            self.log.warning("Planner did not use additional options", kwargs=kwargs)

    def plan_pr(
        self,
        repo: Repo,
        issue: Issue,
    ) -> PullRequestDescription:
        self.log.info("Planning PR", issue=issue)
        pr_desc = self._plan_pr(repo, issue)
        self.log.info("Planned PR", issue=issue, pull_request=pr_desc)
        return pr_desc

    def _plan_pr(
        self,
        repo: Repo,
        issue: Issue,
    ) -> PullRequestDescription:
        raise NotImplementedError

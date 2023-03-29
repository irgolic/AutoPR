from typing import ClassVar, Union

from git.repo import Repo

from autopr.models.artifacts import Issue
from autopr.models.events import IssueCommentEvent, IssueOpenedEvent
from autopr.models.rail_objects import PullRequestDescription
from autopr.services.rail_service import RailService

import structlog


class PullRequestAgentBase:
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        **kwargs,
    ):
        self.rail_service = rail_service

        self.log = structlog.get_logger(agent="pull_request",
                                        id=self.id)
        if kwargs:
            self.log.warning("Planner did not use additional options", kwargs=kwargs)

    def plan_pull_request(
        self,
        repo: Repo,
        issue: Issue,
        event: Union[IssueOpenedEvent, IssueCommentEvent],
    ) -> PullRequestDescription:
        log = self.log.bind(issue_number=issue.number,
                            event_type=event.event_type)
        log.info("Planning PR")
        pull_request = self._plan_pull_request(repo, issue, event)
        if isinstance(pull_request, str):
            log.info("Running raw PR description through PullRequestDescription rail")
            pull_request = self.rail_service.run_rail_object(
                PullRequestDescription,
                pull_request
            )
            if pull_request is None:
                raise ValueError("Failed to parse PR description")
        log.info("Planned PR")
        return pull_request

    def _plan_pull_request(
        self,
        repo: Repo,
        issue: Issue,
        event: Union[IssueOpenedEvent, IssueCommentEvent],
    ) -> Union[str, PullRequestDescription]:
        raise NotImplementedError

from typing import ClassVar, Union

from git.repo import Repo

from autopr.models.artifacts import Issue
from autopr.models.events import EventUnion
from autopr.models.rail_objects import PullRequestDescription
from autopr.services.chain_service import ChainService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService

import structlog


class PullRequestAgentBase:
    """
    Base class for Pull Request agents.
    Pull Request agents are responsible for generating the description of a pull request.
    """

    #: The ID of the agent, used to identify it in the settings. Set it in the subclass.
    id: ClassVar[str]

    def __init__(
        self,
        publish_service: PublishService,
        rail_service: RailService,
        chain_service: ChainService,
        **kwargs,
    ):
        self.publish_service = publish_service
        self.rail_service = rail_service
        self.chain_service = chain_service

        self.log = structlog.get_logger(agent="pull_request",
                                        id=self.id)
        if kwargs:
            self.log.warning("Planner did not use additional options", kwargs=kwargs)

    def plan_pull_request(
        self,
        repo: Repo,
        issue: Issue,
        event: EventUnion,
    ) -> PullRequestDescription:
        log = self.log.bind(issue_number=issue.number,
                            event_type=event.event_type)
        log.info("Planning PR")
        self.publish_service.start_section("▶️ Planning pull request...")
        pull_request = self._plan_pull_request(repo, issue, event)
        if isinstance(pull_request, str):
            log.info("Running raw PR description through PullRequestDescription rail")
            pull_request = self.rail_service.run_rail_object(
                PullRequestDescription,
                pull_request
            )
            if pull_request is None:
                self.publish_service.end_section(title="❌ Failed to plan pull request")
                raise ValueError("Failed to parse PR description")
        self.publish_service.end_section(title="✅ Planned pull request", result=str(pull_request))
        log.info("Planned PR")
        return pull_request

    def _plan_pull_request(
        self,
        repo: Repo,
        issue: Issue,
        event: EventUnion
    ) -> Union[str, PullRequestDescription]:
        """
        Override this method to implement your own pull request planning logic.
        This method should return a PullRequestDescription object, or a string.
        If a string is returned, it will automatically be parsed into a PullRequestDescription object by guardrails.
        """
        raise NotImplementedError

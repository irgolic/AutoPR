import traceback
from typing import ClassVar

from git.repo import Repo

from autopr.agents.codegen_agent import CodegenAgent
from autopr.agents.pull_request_agent import PullRequestAgent
from autopr.models.artifacts import Issue
from autopr.models.events import EventUnion
from autopr.models.rail_objects import PullRequestDescription, CommitPlan
from autopr.services.chain_service import ChainService
from autopr.services.commit_service import CommitService
from autopr.services.diff_service import DiffService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService

import structlog


class BrainAgentBase:
    """
    Base class for Brain agents.
    The Brain is responsible for orchestrating the entire process of generating a pull request by invoking sub-agents.
    """

    #: The ID of the agent, used to identify it in the settings. Set it in the subclass.
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        chain_service: ChainService,
        diff_service: DiffService,
        codegen_agent: CodegenAgent,
        pull_request_agent: PullRequestAgent,
        commit_service: CommitService,
        publish_service: PublishService,
        repo: Repo,
        **kwargs,
    ):
        self.rail_service = rail_service
        self.chain_service = chain_service
        self.diff_service = diff_service
        self.codegen_agent = codegen_agent
        self.pull_request_agent = pull_request_agent
        self.commit_service = commit_service
        self.publish_service = publish_service
        self.repo = repo

        self.log = structlog.get_logger(service="brain",
                                        id=self.id)
        if kwargs:
            self.log.warning("Brain did not use additional options", kwargs=kwargs)

    def generate_pr(
        self,
        event: EventUnion,
    ) -> None:
        # Publish an empty pull request
        self.publish_service.update()

        self.log.info("Generating changes", event_=event)
        try:
            self._generate_pr(event)
        except Exception as e:
            self.log.exception("Failed to generate pull request", event_=event, exc_info=e)
            self.publish_service.finalize(success=False)
            raise e

        self.log.info("Generated changes", event_=event)
        # Finalize the pull request (put progress updates in a collapsible)
        self.publish_service.finalize(success=True)

    def _generate_pr(
        self,
        event: EventUnion,
    ) -> None:
        """
        Override this method to implement your own logic of the Brain agent.
        This method should orchestrate the entire process of generating a pull request.
        """
        raise NotImplementedError

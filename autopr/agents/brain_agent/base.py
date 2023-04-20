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
        self.log.info("Generating changes", event_=event)
        self._generate_pr(event)
        self.log.info("Generated changes", event_=event)

    def _generate_pr(
        self,
        event: EventUnion,
    ) -> None:
        raise NotImplementedError

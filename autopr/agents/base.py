import traceback
from typing import ClassVar, Collection, Type

from git.repo import Repo

from autopr.models.events import EventUnion
from autopr.services.action_service import ActionService
from autopr.services.chain_service import ChainService
from autopr.services.commit_service import CommitService
from autopr.services.diff_service import DiffService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService

import structlog


class Agent:
    """
    Base class for agents.
    An agent is responsible for orchestrating the entire process of generating a pull request by invoking actions.
    """

    #: The ID of the agent, used to identify it in the settings.
    id: ClassVar[str]

    def __init__(
        self,
        rail_service: RailService,
        chain_service: ChainService,
        diff_service: DiffService,
        commit_service: CommitService,
        publish_service: PublishService,
        action_service: ActionService,
        repo: Repo,
        **kwargs,
    ):
        self.rail_service = rail_service
        self.chain_service = chain_service
        self.diff_service = diff_service
        self.commit_service = commit_service
        self.publish_service = publish_service
        self.action_service = action_service
        self.repo = repo

        self.log = structlog.get_logger(service="brain",
                                        id=self.id)
        if kwargs:
            self.log.warning("Agent did not use additional options", kwargs=kwargs)

    def handle_event(
        self,
        event: EventUnion,
    ) -> None:
        """
        Override this method to implement your own logic of the agent.
        This method should orchestrate the entire process of generating a pull request.
        """
        raise NotImplementedError


def get_all_agents(parent=Agent) -> Collection[Type[Agent]]:
    # import to initialize Action subclasses
    import autopr.agents

    descendants = set()
    for subclass in parent.__subclasses__():
        descendants.add(subclass)
        # get subclasses of subclasses
        descendants.update(get_all_agents(subclass))
    return descendants

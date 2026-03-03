from typing import Optional, Any

import structlog
from git.repo import Repo

from autopr.agents.base import Agent, get_all_agents
from autopr.models.events import EventUnion
from autopr.services.action_service import ActionService
from autopr.services.chain_service import ChainService
from autopr.services.commit_service import CommitService
from autopr.services.diff_service import DiffService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService


class AgentService:
    def __init__(
        self,
        rail_service: RailService,
        chain_service: ChainService,
        diff_service: DiffService,
        commit_service: CommitService,
        publish_service: PublishService,
        action_service: ActionService,
        repo: Repo,
    ):
        self.repo = repo
        self.publish_service = publish_service
        self.rail_service = rail_service
        self.chain_service = chain_service
        self.diff_service = diff_service
        self.commit_service = commit_service
        self.action_service = action_service

        # Load all agents in the `autopr/agents` directory
        self.agents: dict[str, type[Agent]] = {
            agent.id: agent
            for agent in get_all_agents()
        }

        self.log = structlog.get_logger(service="agent_service")

    def run_agent(
        self,
        agent_id: str,
        agent_config: Optional[dict[str, Any]],
        event: EventUnion,
    ):
        # Get the agent
        agent_type = self.agents[agent_id]
        agent = agent_type(
            repo=self.repo,
            rail_service=self.rail_service,
            chain_service=self.chain_service,
            diff_service=self.diff_service,
            commit_service=self.commit_service,
            publish_service=self.publish_service,
            action_service=self.action_service,
            **(agent_config or {}),
        )

        # Publish an empty pull request
        self.publish_service.update()

        # Publish a warning if using gpt-3.5-turbo
        if self.rail_service.completions_repo.model == "gpt-3.5-turbo":
            self.publish_service.publish_update(
                "⚠️⚠️⚠️ Warning: Using `gpt-3.5-turbo` completion model. "
                "AutoPR is currently not optimized for this model. "
                "See https://github.com/irgolic/AutoPR/issues/65 for more details. "
                "In the mean time, if you have access to the `gpt-4` API, please use that instead. "
                "Please note that ChatGPT Plus does not give you access to the `gpt-4` API; "
                "you need to sign up on [the GPT-4 API waitlist](https://openai.com/waitlist/gpt-4-api). "
            )

        self.log.info("Generating changes", event_=event)
        try:
            agent.handle_event(event)
        except Exception as e:
            self.log.exception("Agent failed", event_=event, exc_info=e)
            self.publish_service.finalize(success=False)
            raise e

        self.log.info("Generated changes", event_=event)

        # Finalize the pull request (put progress updates in a collapsible)
        self.publish_service.finalize(success=True)

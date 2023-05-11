from typing import Optional, Any

import openai
from git.repo import Repo
from pydantic import BaseSettings

from .models.artifacts import Issue
from .models.events import EventUnion
from .repos.completions_repo import OpenAICompletionsRepo, OpenAIChatCompletionsRepo, get_completions_repo
from .services.action_service import ActionService
from .services.agent_service import AgentService
from .services.chain_service import ChainService
from .services.commit_service import CommitService
from .services.diff_service import GitApplyService, PatchService
from .services.event_service import EventService, GitHubEventService
from .services.publish_service import GitHubPublishService, PublishService
from .services.rail_service import RailService

import structlog

log = structlog.get_logger()


class Settings(BaseSettings):
    agent_id: str = 'simple'
    agent_config: Optional[dict[str, Any]] = None

    base_branch: str = 'main'
    target_branch_name_template: str = 'autopr/{issue_number}'
    loading_gif_url: str = "https://media0.giphy.com/media/l3nWhI38IWDofyDrW/giphy.gif"
    model: str = "gpt-4"
    temperature: float = 0.8
    rail_temperature: float = 0.4
    context_limit: int = 8192
    min_tokens: int = 1000
    max_tokens: int = 2000
    num_reasks: int = 2


def main(
    repo_path: str,
    event: EventUnion,
    commit_service: CommitService,
    publish_service: PublishService,
    settings: Settings,
):
    log.info('Starting main',
             repo_path=repo_path,
             settings=settings)

    # Instantiate repo
    repo = Repo(repo_path)

    # Checkout base branch
    log.debug(f'Checking out {settings.base_branch}...')
    repo.heads[settings.base_branch].checkout()

    # Pull latest changes
    log.debug('Pulling latest changes...')
    repo.remotes.origin.pull()

    # Create completions repo
    completions_repo = get_completions_repo(
        publish_service=publish_service,
        model=settings.model,
        context_limit=settings.context_limit,
        min_tokens=settings.min_tokens,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )

    # Create the new branch
    commit_service.overwrite_new_branch()

    # Create rail and chain service
    rail_service = RailService(
        completions_repo=completions_repo,
        min_tokens=settings.min_tokens,
        context_limit=settings.context_limit,
        num_reasks=settings.num_reasks,
        temperature=settings.rail_temperature,
        publish_service=publish_service,
    )
    chain_service = ChainService(
        completions_repo=completions_repo,
        publish_service=publish_service,
        context_limit=settings.context_limit,
        min_tokens=settings.min_tokens,
    )

    # Create diff service
    diff_service = GitApplyService(repo=repo)

    # Create action service and agent service
    action_service = ActionService(
        repo=repo,
        completions_repo=completions_repo,
        rail_service=rail_service,
        publish_service=publish_service,
        chain_service=chain_service,
    )
    agent_service = AgentService(
        repo=repo,
        publish_service=publish_service,
        rail_service=rail_service,
        chain_service=chain_service,
        diff_service=diff_service,
        commit_service=commit_service,
        action_service=action_service,
    )

    # Generate and set_pr_description the PR
    agent_service.run_agent(settings.agent_id, settings.agent_config, event)

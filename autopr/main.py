from typing import Optional, Any

import openai
from git.repo import Repo
from pydantic import BaseSettings

from .agents.brain_agent import get_brain_agent
from .models.artifacts import Issue
from .models.events import EventUnion
from .repos.completions_repo import OpenAICompletionsRepo, OpenAIChatCompletionsRepo, get_completions_repo
from .services.chain_service import ChainService
from .services.commit_service import CommitService
from .services.diff_service import GitApplyService, PatchService
from .services.event_service import EventService, GithubEventService
from .services.publish_service import GithubPublishService, PublishService
from .services.rail_service import RailService
from .agents.codegen_agent import get_codegen_agent
from .agents.pull_request_agent import get_pull_request_agent

from .validators import create_unidiff_validator

import structlog

log = structlog.get_logger()


class Settings(BaseSettings):
    pull_request_agent_id: str = 'rail-v1'
    pull_request_agent_config: Optional[dict[str, Any]] = None
    codegen_agent_id: str = 'auto-v1'
    codegen_agent_config: Optional[dict[str, Any]] = None
    brain_agent_id: str = 'simple-v1'
    brain_agent_config: Optional[dict[str, Any]] = None

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
    )

    # auto-v1 generates diffs with `git diff`, so use that
    if settings.codegen_agent_id == 'auto-v1':
        diff_service = GitApplyService(repo=repo)
    else:
        diff_service = PatchService(repo=repo)

    # Instantiate the agents
    codegen_agent = get_codegen_agent(
        publish_service=publish_service,
        codegen_agent_id=settings.codegen_agent_id,
        rail_service=rail_service,
        chain_service=chain_service,
        diff_service=diff_service,
        repo=repo,
        extra_params=settings.codegen_agent_config,
    )
    pull_request_agent = get_pull_request_agent(
        publish_service=publish_service,
        pull_request_agent_id=settings.pull_request_agent_id,
        rail_service=rail_service,
        chain_service=chain_service,
        extra_params=settings.pull_request_agent_config,
    )
    brain_agent = get_brain_agent(
        brain_agent_id=settings.brain_agent_id,
        codegen_agent=codegen_agent,
        pull_request_agent=pull_request_agent,
        rail_service=rail_service,
        commit_service=commit_service,
        publish_service=publish_service,
        diff_service=diff_service,
        chain_service=chain_service,
        repo=repo,
    )

    # Create validators for guardrails
    create_unidiff_validator(repo, diff_service)

    # Generate and set_pr_description the PR
    brain_agent.generate_pr(event)

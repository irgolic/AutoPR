from typing import Optional, Any

import openai
from git.repo import Repo
from pydantic import BaseSettings

from .models.artifacts import Issue
from .repos.completions_repo import OpenAICompletionsRepo, OpenAIChatCompletionsRepo, get_completions_repo
from .services.chain_service import ChainService
from .services.commit_service import CommitService
from .services.diff_service import GitApplyService, PatchService
from .services.event_service import EventService
from .services.generation_service import GenerationService
from .services.publish_service import GithubPublishService
from .services.rail_service import RailService
from .agents.codegen_agent import get_codegen_agent
from .agents.pull_request_agent import get_pull_request_agent

from .validators import create_unidiff_validator, create_filepath_validator

import structlog

log = structlog.get_logger()


class Settings(BaseSettings):
    github_token: str
    base_branch: str
    event_name: str
    event: dict[str, Any]
    target_branch_name_template: str = 'autopr/{issue_number}'
    pull_request_agent_id: str = 'rail-v1'
    pull_request_agent_config: Optional[dict[str, Any]] = None
    codegen_agent_id: str = 'auto-v1'
    codegen_agent_config: Optional[dict[str, Any]] = None
    model: str = "gpt-4"
    temperature: float = 0.8
    rail_temperature: float = 0.4
    context_limit: int = 8192
    min_tokens: int = 1000
    max_tokens: int = 2000
    num_reasks: int = 2


def main(
    repo_path: str,
    settings: Settings,
):
    log.info('Starting main',
             repo_path=repo_path,
             settings=settings)

    # Extract event
    event_service = EventService(
        github_token=settings.github_token,
    )
    event_obj = event_service.from_github_event(settings.event_name, settings.event)
    issue = event_obj.issue

    # Format branch name
    branch_name = settings.target_branch_name_template.format(issue_number=issue.number)

    # Instantiate repo
    repo = Repo(repo_path)

    # Checkout base branch
    log.debug(f'Checking out {settings.base_branch}...')
    repo.heads[settings.base_branch].checkout()

    # Pull latest changes
    log.debug('Pulling latest changes...')
    repo.remotes.origin.pull()

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    # Create completions repo
    completions_repo = get_completions_repo(
        model=settings.model,
        context_limit=settings.context_limit,
        min_tokens=settings.min_tokens,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
    )

    # Create services and agents
    rail_service = RailService(
        completions_repo=completions_repo,
        min_tokens=settings.min_tokens,
        context_limit=settings.context_limit,
        num_reasks=settings.num_reasks,
        temperature=settings.rail_temperature,
    )
    chain_service = ChainService(
        completions_repo=completions_repo,
    )

    # auto-v1 generates diffs with `git diff`, so use that
    if settings.codegen_agent_id == 'auto-v1':
        diff_service = GitApplyService(repo=repo)
    else:
        diff_service = PatchService(repo=repo)

    codegen_agent = get_codegen_agent(
        codegen_agent_id=settings.codegen_agent_id,
        rail_service=rail_service,
        chain_service=chain_service,
        diff_service=diff_service,
        repo=repo,
        extra_params=settings.codegen_agent_config,
    )
    pull_request_agent = get_pull_request_agent(
        pull_request_agent_id=settings.pull_request_agent_id,
        rail_service=rail_service,
        chain_service=chain_service,
        extra_params=settings.pull_request_agent_config,
    )
    commit_service = CommitService(
        repo=repo,
        repo_path=repo_path,
        branch_name=branch_name,
        base_branch_name=settings.base_branch,
    )
    publish_service = GithubPublishService(
        token=settings.github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=settings.base_branch,
    )
    generator_service = GenerationService(
        codegen_agent=codegen_agent,
        pull_request_agent=pull_request_agent,
        rail_service=rail_service,
        commit_service=commit_service,
        publish_service=publish_service,
    )

    # Create validators for guardrails
    create_unidiff_validator(repo, diff_service)
    create_filepath_validator(repo)

    # Generate and publish the PR
    generator_service.generate_pr(repo, issue, event_obj)

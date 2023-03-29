from typing import Optional, Any

import openai
from git.repo import Repo

from .models.artifacts import Issue
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


def main(
    github_token: str,
    repo_path: str,
    base_branch: str,
    event_name: str,
    event: dict[str, Any],
    codegen_agent_id: str = "rail-v1",
    pull_request_agent_id: str = "rail-v1",
    model: str = "gpt-4",
    context_limit: int = 8192,
    min_tokens: int = 1000,
    max_tokens: int = 2000,
    num_reasks: int = 2,
    **kwargs,
):
    log.info('Starting main',
             repo_path=repo_path,
             base_branch_name=base_branch,
             gh_event_name=event_name,
             gh_event=event)

    # Extract event
    event_service = EventService(
        github_token=github_token,
    )
    event_obj = event_service.from_github_event(event_name, event)
    issue = event_obj.issue

    branch_name = f'autopr/{issue.number}'
    repo = Repo(repo_path)

    # Checkout base branch
    log.debug(f'Checking out {base_branch}...')
    repo.heads[base_branch].checkout()

    # Pull latest changes
    log.debug('Pulling latest changes...')
    repo.remotes.origin.pull()

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    if any(name in model
           for name in ("davinci", "curie", "babbage", "ada")):
        completion_func = openai.Completion.create
    else:
        completion_func = openai.ChatCompletion.create

    # Create services and agents
    rail_service = RailService(
        completion_model=model,
        completion_func=completion_func,
        context_limit=context_limit,
        min_tokens=min_tokens,
        max_tokens=max_tokens,
        num_reasks=num_reasks,
    )
    diff_service = PatchService(repo=repo)
    codegen_agent = get_codegen_agent(
        codegen_agent_id=codegen_agent_id,
        diff_service=diff_service,
        rail_service=rail_service,
        repo=repo,
        extra_params=kwargs,
    )
    pull_request_agent = get_pull_request_agent(
        pull_request_agent_id=pull_request_agent_id,
        rail_service=rail_service,
        extra_params=kwargs,
    )
    commit_service = CommitService(
        diff_service=diff_service,
        repo=repo,
        repo_path=repo_path,
        branch_name=branch_name,
        base_branch_name=base_branch,
    )
    publish_service = GithubPublishService(
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=base_branch,
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

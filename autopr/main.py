from typing import Optional, Any

import openai
from git.repo import Repo

from .models.artifacts import Issue
from .services.codegen_service import get_codegen_service
from .services.commit_service import CommitService
from .services.diff_service import GitApplyService, PatchService
from .services.generation_service import GenerationService
from .services.planner_service import get_planner_service
from .services.publish_service import GithubPublishService
from .services.rail_service import RailService

from .validators import create_unidiff_validator, create_filepath_validator

import structlog

log = structlog.get_logger()


def main(
    github_token: str,
    repo_path: str,
    base_branch: str,
    issue_number: int,
    issue_title: str,
    issue_body: str,
    codegen_id: str = "rail-v1",
    planner_id: str = "rail-v1",
    model: str = "gpt-4",
    context_limit: int = 8192,
    min_tokens: int = 1000,
    max_tokens: int = 2000,
    num_reasks: int = 2,
    **kwargs,
):
    log.info('Starting main', repo_path=repo_path, base_branch_name=base_branch,
             issue_number=issue_number, issue_title=issue_title, issue_body=issue_body)
    branch_name = f'autopr/issue-{issue_number}'
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

    # Create models
    issue = Issue(
        number=issue_number,
        title=issue_title,
        body=issue_body,
    )

    # Create services
    rail_service = RailService(
        completion_model=model,
        completion_func=completion_func,
        context_limit=context_limit,
        min_tokens=min_tokens,
        max_tokens=max_tokens,
        num_reasks=num_reasks,
    )
    diff_service = PatchService(repo=repo)
    codegen_service = get_codegen_service(
        codegen_id=codegen_id,
        diff_service=diff_service,
        rail_service=rail_service,
        repo=repo,
        extra_params=kwargs,
    )
    planner_service = get_planner_service(
        planner_id=planner_id,
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
        codegen_service=codegen_service,
        planner_service=planner_service,
        rail_service=rail_service,
        commit_service=commit_service,
        publish_service=publish_service,
    )

    # Create validators for guardrails
    create_unidiff_validator(repo, diff_service)
    create_filepath_validator(repo)

    # Generate and publish the PR
    generator_service.generate_pr(repo, issue)

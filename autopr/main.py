import openai
from git import Repo
from autopr.services.pull_request_service import GithubPullRequestService
from .models.rail_objects import PullRequestDescription
from .models.repo import RepoCommit
from .services.commit_service import CommitService
from .services.diff_service import GitApplyService, PatchService
from .services.generation_service import GenerationService
from .services.rail_service import RailService

from .validators import create_unidiff_validator, create_filepath_validator

import structlog

log = structlog.get_logger()


def main(
    github_token: str,
    repo_path: str,
    base_branch_name: str,
    issue_number: int,
    issue_title: str,
    issue_body: str,
    model: str = "gpt-4",
    context_limit: int = 8192,
    min_tokens: int = 1000,
    max_tokens: int = 2000,
    num_reasks: int = 2,
):
    log.info('Starting main', repo_path=repo_path, base_branch_name=base_branch_name,
             issue_number=issue_number, issue_title=issue_title, issue_body=issue_body)
    branch_name = f'autopr/issue-{issue_number}'
    repo = Repo(repo_path)

    # Checkout base branch
    log.debug(f'Checking out {base_branch_name}...')
    repo.heads[base_branch_name].checkout()

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

    # Create services
    rail_service = RailService(
        completion_model=model,
        completion_func=completion_func,
        context_limit=context_limit,
        min_tokens=min_tokens,
        max_tokens=max_tokens,
        num_reasks=num_reasks,
    )
    generator = GenerationService(
        rail_service=rail_service,
    )
    pr_service = GithubPullRequestService(
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=base_branch_name,
    )
    diff_service = PatchService(repo=repo)
    commit_service = CommitService(
        repo=repo,
        diff_service=diff_service,
        repo_path=repo_path,
        branch_name=branch_name,
        base_branch_name=base_branch_name,
    )

    # Create validators for guardrails
    create_unidiff_validator(repo, diff_service)
    create_filepath_validator(repo)

    # Create/Overwrite branch
    commit_service.switch_to_branch()

    pr_pushed = False

    def handle_commit(pull_request: PullRequestDescription, commit: RepoCommit):
        nonlocal pr_pushed

        commit_service.commit(commit)

        if not pr_pushed:
            # Create PR
            log.debug('Creating PR...')
            pr_service.publish(pull_request)
            pr_pushed = True

    # Generate PR commits, title, and body
    log.debug('Generating PR...')
    generator.generate_pr(repo, issue_title, issue_body, issue_number, handle_commit=handle_commit)

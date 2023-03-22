import os
import tempfile


from git import Repo
from autopr.services.pull_request_service import GithubPullRequestService
from .models.rail_objects import PullRequestDescription
from .models.repo import RepoCommit
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

    # Create validators for guardrails
    create_unidiff_validator(repo)
    create_filepath_validator(repo)

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    # Create services
    rail_service = RailService(
        completion_model=model,
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

    # If branch already exists, delete it
    if branch_name in repo.heads:
        print(f'Deleting existing branch {branch_name}...')
        repo.delete_head(branch_name, force=True)

    # Create new branch with create_new_ref
    log.debug(f'Creating new branch {branch_name}...')
    repo.create_head(branch_name, base_branch_name)

    # Checkout new branch
    repo.heads[branch_name].checkout()

    pr_pushed = False

    def handle_commit(pull_request: PullRequestDescription, commit: RepoCommit):
        nonlocal pr_pushed

        # Remove guardrails log if exists (so it's not committed later)
        if 'guardrails.log' in repo.untracked_files:
            log.debug('Removing guardrails.log...')
            os.remove(
                os.path.join(repo_path, 'guardrails.log')
            )

        # Apply diff
        diff = commit.diff
        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            f.flush()
            log.debug('Applying diff...')
            repo.git.execute(["git",
                              "apply",
                              "--unidiff-zero",
                              "--inaccurate-eof",
                              "--allow-empty",
                              f.name])

        # Add and commit all
        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "--allow-empty", "-m", commit.message])

        # Push branch to remote
        log.debug(f'Pushing branch {branch_name} to remote...')
        repo.git.execute(["git", "push", "-f", "origin", branch_name])

        if not pr_pushed:
            # Create PR
            log.debug('Creating PR...')
            pr_service.publish(pull_request)
            pr_pushed = True

    # Generate PR commits, title, and body
    log.debug('Generating PR...')
    generator.generate_pr(repo, issue_title, issue_body, issue_number, handle_commit=handle_commit)

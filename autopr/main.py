import os
import tempfile


from git import Repo
from autopr.services.pull_request_service import GithubPullRequestService
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

    tree = repo.heads[base_branch_name].commit.tree

    # Create validators for guardrails
    create_unidiff_validator(repo, tree)
    create_filepath_validator(tree)

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    # Create generator service
    rail_service = RailService()
    generator = GenerationService(
        rail_service=rail_service,
    )

    # Generate PR commits, title, and body
    tree = repo.heads[base_branch_name].commit.tree
    log.debug('Generating PR...')
    pr = generator.generate_pr(tree, issue_title, issue_body, issue_number)

    # Remove guardrails log if exists (so it's not committed later)
    if 'guardrails.log' in repo.untracked_files:
        log.debug('Removing guardrails.log...')
        os.remove(
            os.path.join(repo_path, 'guardrails.log')
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

    # Create new commits with create_new_commit
    for commit in pr.commits:
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

        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "--allow-empty", "-m", commit.message])

    # Push branch to remote
    log.debug(f'Pushing branch {branch_name} to remote...')
    repo.git.execute(["git", "push", "-f", "origin", branch_name])

    # Create PR
    pr_service = GithubPullRequestService(
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=base_branch_name,
    )
    log.debug('Creating PR...')
    pr_service.publish(pr)

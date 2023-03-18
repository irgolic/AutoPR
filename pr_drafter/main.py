import tempfile


from git import Repo
from pr_drafter.services.generation_service import RailsGenerationService
from pr_drafter.services.pull_request_service import GithubPullRequestService

from .validators import create_unidiff_validator, create_filepath_validator


def main(
    github_token: str,
    repo_path: str,
    base_branch_name: str,
    issue_number: int,
    issue_title: str,
    issue_body: str,
):
    branch_name = f'autopr/issue-{issue_number}'
    repo = Repo(repo_path)
    tree = repo.heads[base_branch_name].commit.tree

    # Create validators for guardrails
    create_unidiff_validator(repo, tree)
    create_filepath_validator(tree)

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    # Create generator service
    generator = RailsGenerationService()

    # Checkout base branch
    print(f'Checking out {base_branch_name}...')
    repo.heads[base_branch_name].checkout()

    # Pull latest changes
    print('Pulling latest changes...')
    repo.remotes.origin.pull()

    # Generate PR commits, title, and body
    tree = repo.heads[base_branch_name].commit.tree
    print('Generating PR...')
    pr = generator.generate_pr(tree, issue_title, issue_body, issue_number)

    # If branch already exists, delete it
    if branch_name in repo.heads:
        print(f'Deleting existing branch {branch_name}...')
        repo.delete_head(branch_name, force=True)

    # Create new branch with create_new_ref
    print(f'Creating new branch {branch_name}...')
    repo.create_head(branch_name, base_branch_name)

    # Checkout new branch
    repo.heads[branch_name].checkout()

    # Create new commits with create_new_commit
    for commit in pr.commits:
        diff = commit.diff

        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            f.flush()
            print('Applying diff...')
            repo.git.execute(["git", "apply", f.name])

        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "-m", commit.message])

    # Push branch to remote
    print(f'Pushing branch {branch_name} to remote...')
    repo.git.execute(["git", "push", "-f", "origin", branch_name])

    # Create PR
    pr_service = GithubPullRequestService(
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=base_branch_name,
    )
    print('Creating PR...')
    pr_service.publish(pr)

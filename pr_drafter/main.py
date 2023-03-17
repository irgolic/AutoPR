import tempfile


from git import Repo
from pr_drafter.services.generation_service import RailsGenerationService
from pr_drafter.services.pull_request_service import GithubPullRequestService

from validators import create_unidiff_validator


def main(
    github_token: str,
    repo_path: str,
    base_branch_name: str,
    issue_number: int,
    issue_title: str,
    issue_body: str,
):
    repo = Repo(repo_path)
    branch_name = f'autopr/issue-{issue_number}'

    # Create unidiff validator for guardrails
    create_unidiff_validator(repo)

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.split('/')[-2:]

    # Initialize services
    pr_service = GithubPullRequestService(
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=base_branch_name,
    )
    generator = RailsGenerationService()

    # Checkout base branch
    repo.heads[base_branch_name].checkout()

    # If branch already exists, delete it
    if branch_name in repo.heads:
        repo.delete_head(branch_name)

    # Generate PR commits, title, and body
    tree = repo.heads[base_branch_name].commit.tree
    pr = generator.generate_pr(tree, issue_title, issue_body)

    # Create new branch with create_new_ref
    repo.create_head(branch_name, base_branch_name)

    # Checkout new branch
    repo.heads[branch_name].checkout()

    # Create new commits with create_new_commit
    for commit in pr.commits:
        diff = commit.diff

        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            f.flush()
            repo.git.execute(["git", "apply", f.name])

        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "-m", commit.message])

    # Push branch to remote
    repo.git.execute(["git", "push", "origin", branch_name])

    # Create PR
    pr_service.publish(pr)

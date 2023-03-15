import tempfile

from git import Repo
from pr_drafter.rails import generate_pr


def main(
    repo_path: str,
    base_branch_name: str,
    issue_number: int,
    issue_title: str,
    issue_body: str,
):
    repo = Repo(repo_path)
    branch_name = f'autopr-issue-{issue_number}'

    # If branch already exists, delete it
    if branch_name in repo.heads:
        repo.delete_head(branch_name)

    # Generate PR commits, title, and body
    tree = repo.heads[base_branch_name].commit.tree
    pr = generate_pr(tree, issue_title, issue_body)

    # Create new branch with create_new_ref
    repo.create_head(branch_name, base_branch_name)

    # Create new commits with create_new_commit
    for commit in pr.commits:
        diff = commit.diff

        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            repo.git.execute(["git", "apply", f.name])

        repo.git.execute(["git", "add", "."])
        repo.git.execute(["git", "commit", "-m", commit.message])

    # Push branch to remote
    repo.git.execute(["git", "push", "origin", branch_name])

import os
import git
import tempfile


git_dir = os.environ.get("GIT_REPOSITORY_PATH")
if git_dir is None:
    os.mkdir("tmp")
    git_dir = 'tmp/repo'


# def pull_git_repo(url: str):
#     git.repo.base.Repo.clone_from(url, git_dir)


def apply_git_diff(diff: str):
    repo = git.Repo(git_dir)
    with tempfile.NamedTemporaryFile() as f:
        f.write(diff.encode())
        repo.git.execute(["git", "apply", f.name])

import os
from typing import Optional, Literal

from git.repo import Repo

from autopr.log_config import get_logger


CHANGES_STATUS = Literal["no_changes", "cache_only", "modified"]


class CommitService:
    """
    Service for creating branches, committing changes, and calling `git push` on the repository.

    Ensures there is always a commit on the branch.
    """

    def __init__(
        self,
        repo: Repo,
        repo_path: str,
        branch_name: str,
        base_branch_name: str,
        cache_dir: str,
    ):
        self.repo = repo
        self.repo_path = repo_path
        self.branch_name = branch_name
        self.base_branch_name = base_branch_name
        self.cache_dir = cache_dir

        self._empty_commit_message = "[placeholder]"

        self.log = get_logger(service="commit")

    def overwrite_new_branch(self):
        # Checkout and pull base branch
        self.log.debug(f'Checking out {self.base_branch_name}...')
        self.repo.heads[self.base_branch_name].checkout()
        self.log.debug('Pulling latest changes...')
        self.repo.remotes.origin.pull()

        # If branch already exists, delete it
        if self.branch_name in self.repo.heads:
            self.log.debug(f'Deleting existing branch {self.branch_name}...')
            self.repo.delete_head(self.branch_name, force=True)

        # Create new branch with create_new_ref
        self.log.debug(f'Creating new branch {self.branch_name}...')
        self.repo.create_head(self.branch_name, self.base_branch_name)

        # Checkout new branch
        self.repo.heads[self.branch_name].checkout()

        # Create empty commit
        self.commit(self._empty_commit_message)

    def ensure_branch_exists(self):
        # Fetch
        self.log.debug('Fetching...')
        self.repo.remotes.origin.fetch()
        remote = self.repo.remote()
        references = remote.fetch()

        # If branch already exists, checkout and pull
        if f'{remote.name}/{self.branch_name}' in [ref.name for ref in references]:
            # Check if branch exists locally
            if self.branch_name in [ref.name for ref in self.repo.heads]:
                self.log.debug(f'Checking out {self.branch_name}...')
                self.repo.heads[self.branch_name].checkout()
                self.log.debug('Pulling latest changes...')
                self.repo.remotes.origin.pull()
            else:
                # If not, create a local branch that tracks the remote branch
                self.log.debug(f'Checking out -b {self.branch_name}...')
                self.repo.create_head(self.branch_name, f'{remote.name}/{self.branch_name}').checkout()
        else:
            self.log.debug(f'Branch {self.branch_name} does not exist, creating...')
            self.overwrite_new_branch()

    def commit(
        self,
        commit_message: str,
        push: bool = True,
        filepaths: Optional[list[str]] = None,
    ) -> None:
        # Remove empty commit if exists
        if commit_message != self._empty_commit_message and \
                self.repo.head.commit.message.rstrip() == self._empty_commit_message:
            self.log.debug('Removing empty commit...')
            self.repo.git.execute(["git", "reset", "HEAD^"])

        # Add and commit
        if filepaths is None:
            self.repo.git.execute(["git", "add", "-A"])
        else:
            self.repo.git.execute(["git", "add", *filepaths])
        self.repo.git.execute(["git", "commit", "--allow-empty", "-m", commit_message])

        # Get the commit's diff for log
        diff = self.repo.git.execute(["git", "diff", "HEAD^", "HEAD"])
        self.log.info("Committed changes", commit_message=commit_message, diff=diff)

        # Push branch to remote
        if push:
            self.log.debug(f'Pushing branch {self.branch_name} to remote...')
            self.repo.git.execute(["git", "push", "-f", "origin", self.branch_name])

    def get_changes_status(self) -> CHANGES_STATUS:
        """
        Returns the status of the changes on the branch.
        """
        # Get status of changes
        status = self.repo.git.execute(["git", "status", "--porcelain"])
        status_text = str(status)
        if status == "":
            return "no_changes"
        elif len(status_text.splitlines()) == 1 and self.cache_dir in status_text:
            return "cache_only"
        else:
            return "modified"

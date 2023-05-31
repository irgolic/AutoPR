import os

from git.repo import Repo

import structlog


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
    ):
        self.repo = repo
        self.repo_path = repo_path
        self.branch_name = branch_name
        self.base_branch_name = base_branch_name

        self._empty_commit_message = "[placeholder]"

        self.log = structlog.get_logger(service="commit")

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
            self.log.debug(f'Checking out {self.branch_name}...')
            self.repo.heads[self.branch_name].checkout()
            self.log.debug('Pulling latest changes...')
            self.repo.remotes.origin.pull()
        else:
            self.log.debug(f'Branch {self.branch_name} does not exist, creating...')
            self.overwrite_new_branch()

    def commit(self, commit_message: str, push: bool = True) -> None:
        # Remove empty commit if exists
        if commit_message != self._empty_commit_message and \
                self.repo.head.commit.message.rstrip() == self._empty_commit_message:
            self.log.debug('Removing empty commit...')
            self.repo.git.execute(["git", "reset", "HEAD^"])

        # Remove guardrails log if exists (so it's not committed later)
        if 'guardrails.log' in self.repo.untracked_files:
            self.log.debug('Removing guardrails.log...')
            os.remove(
                os.path.join(self.repo_path, 'guardrails.log')
            )

        # Add and commit all
        self.repo.git.execute(["git", "add", "."])
        self.repo.git.execute(["git", "commit", "--allow-empty", "-m", commit_message])

        # Get the commit's diff for log
        diff = self.repo.git.execute(["git", "diff", "HEAD^", "HEAD"])
        self.log.info("Committed changes", commit_message=commit_message, diff=diff)

        # Push branch to remote
        if push:
            self.log.debug(f'Pushing branch {self.branch_name} to remote...')
            self.repo.git.execute(["git", "push", "-f", "origin", self.branch_name])

import os

from git.repo import Repo

import structlog

from autopr.models.artifacts import DiffStr
from autopr.models.rail_objects import CommitPlan
from autopr.services.diff_service import DiffService


class CommitService:
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

        self.is_published = False
        self._empty_commit = CommitPlan(
            commit_message="[empty]",
        )

        self.log = structlog.get_logger(service="commit")

    def overwrite_new_branch(self):
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
        self.commit(self._empty_commit)

    def commit(self, commit: CommitPlan, push: bool = True) -> None:
        # Remove empty commit if exists
        if commit is not self._empty_commit and self.repo.head.commit.message == self._empty_commit.commit_message:
            self.log.debug('Removing empty commit...')
            self.repo.git.execute(["git", "reset", "--hard", "HEAD^"])

        # Remove guardrails log if exists (so it's not committed later)
        if 'guardrails.log' in self.repo.untracked_files:
            self.log.debug('Removing guardrails.log...')
            os.remove(
                os.path.join(self.repo_path, 'guardrails.log')
            )

        # Add and commit all
        self.repo.git.execute(["git", "add", "."])
        self.repo.git.execute(["git", "commit", "--allow-empty", "-m", commit.commit_message])

        # Get the commit's diff for log
        diff = self.repo.git.execute(["git", "diff", "HEAD^", "HEAD"])
        self.log.info("Committed changes", commit_message=commit.commit_message, diff=diff)

        # Push branch to remote
        if push:
            self.log.debug(f'Pushing branch {self.branch_name} to remote...')
            self.repo.git.execute(["git", "push", "-f", "origin", self.branch_name])

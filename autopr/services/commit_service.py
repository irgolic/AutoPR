import os

from git.repo import Repo

import structlog

from autopr.models.artifacts import DiffStr
from autopr.models.rail_objects import CommitPlan
from autopr.services.diff_service import DiffService

log = structlog.get_logger()


class CommitService:
    def __init__(
        self,
        diff_service: DiffService,
        repo: Repo,
        repo_path: str,
        branch_name: str,
        base_branch_name: str,
    ):
        self.diff_service = diff_service
        self.repo = repo
        self.repo_path = repo_path
        self.branch_name = branch_name
        self.base_branch_name = base_branch_name

        self.is_published = False

    def overwrite_new_branch(self):
        # If branch already exists, delete it
        if self.branch_name in self.repo.heads:
            log.debug(f'Deleting existing branch {self.branch_name}...')
            self.repo.delete_head(self.branch_name, force=True)

        # Create new branch with create_new_ref
        log.debug(f'Creating new branch {self.branch_name}...')
        self.repo.create_head(self.branch_name, self.base_branch_name)

        # Checkout new branch
        self.repo.heads[self.branch_name].checkout()

    def commit(self, commit: CommitPlan, diff: DiffStr) -> None:
        # Apply diff
        self.diff_service.apply_diff(diff)

        # Remove guardrails log if exists (so it's not committed later)
        if 'guardrails.log' in self.repo.untracked_files:
            log.debug('Removing guardrails.log...')
            os.remove(
                os.path.join(self.repo_path, 'guardrails.log')
            )

        # Add and commit all
        self.repo.git.execute(["git", "add", "."])
        self.repo.git.execute(["git", "commit", "--allow-empty", "-m", commit.commit_message])

        # Push branch to remote
        log.debug(f'Pushing branch {self.branch_name} to remote...')
        self.repo.git.execute(["git", "push", "-f", "origin", self.branch_name])

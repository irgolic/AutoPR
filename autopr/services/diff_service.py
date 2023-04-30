import tempfile
from typing import Optional

import structlog
from git.repo import Repo

from autopr.models.artifacts import DiffStr

log = structlog.get_logger()


class DiffService:
    """
    Service for getting and applying diffs.

    Diffs are represented as `DiffStr` (a type alias for `str`).
    """
    def __init__(
        self,
        repo: Repo,
    ):
        self.repo = repo

    def apply_diff(self, diff: DiffStr, check: bool = False) -> None:
        raise NotImplementedError()

    def get_diff(self, filepaths: Optional[list[str]] = None) -> DiffStr:
        if not filepaths:
            # Add all files in repo
            self.repo.git.execute(["git", "add", "-A"])
        else:
            # Add specific files
            self.repo.git.execute(["git", "add", *filepaths])
        # Get diff
        diff = self.repo.git.execute(["git", "diff", "--staged"])
        # Reset staged files
        self.repo.git.execute(["git", "reset", "HEAD"])
        return DiffStr(diff)


class GitApplyService(DiffService):
    def apply_diff(self, diff: DiffStr, check: bool = False) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            f.flush()
            log.debug('Applying diff...')
            self.repo.git.execute(["git",
                                   "apply",
                                   "--allow-empty",
                                   f.name])


class PatchService(DiffService):
    def apply_diff(self, diff: DiffStr, check: bool = False) -> None:
        with tempfile.NamedTemporaryFile(suffix=".diff") as f:
            f.write(diff.encode())
            f.flush()
            log.debug('Applying diff...')
            commands = [
                "patch",
                "--no-backup-if-mismatch",
                "--ignore-whitespace",
                "-p0",
                "--force",
                "-i",
                f.name
            ]
            if check:
                commands += ["--dry-run"]
            self.repo.git.execute(commands)

import tempfile

import structlog
from git.repo import Repo

from autopr.models.artifacts import DiffStr

log = structlog.get_logger()


class DiffService:
    def __init__(
        self,
        repo: Repo,
    ):
        self.repo = repo

    def apply_diff(self, diff: DiffStr, check: bool = False) -> None:
        raise NotImplementedError()


class GitApplyService(DiffService):
    def apply_diff(self, diff: DiffStr, check: bool = False) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write(diff.encode())
            f.flush()
            log.debug('Applying diff...')
            self.repo.git.execute(["git",
                                   "apply",
                                   "--unidiff-zero",
                                   "--inaccurate-eof",
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

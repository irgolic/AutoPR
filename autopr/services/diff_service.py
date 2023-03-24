import tempfile

import git
import structlog

log = structlog.get_logger()


class DiffService:
    def __init__(
        self,
        repo: git.Repo,
    ):
        self.repo = repo

    def apply_diff(self, diff: str, check: bool = False) -> None:
        raise NotImplementedError()


class GitApplyService(DiffService):
    def apply_diff(self, diff: str, check: bool = False) -> None:
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
    def apply_diff(self, diff: str, check: bool = False) -> None:
        with tempfile.NamedTemporaryFile(suffix=".diff") as f:
            f.write(diff.encode())
            f.flush()
            log.debug('Applying diff...')
            commands = ["patch"]
            if check:
                commands += ["--dry-run"]
            commands += [
                "--ignore-whitespace",
                "-p0",
                "--force",
                "-i",
                f.name
            ]
            self.repo.git.execute(commands)

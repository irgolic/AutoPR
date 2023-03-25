







from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \
    Diff, CommitPlan
from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \
from pathlib import Path
    NewDiff, FileDescriptor
from autopr.models.repo import RepoCommit
from autopr.models.repo import RepoPullRequest
from autopr.services.rail_service import RailService

import structlog
log = structlog.get_logger()







    ):
        self.rail_service = rail_service
        self.file_context_token_limit = file_context_token_limit
        self.file_chunk_size = file_chunk_size
        self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=8192)
        self.create_gptignore()

    @staticmethod
    def repo_to_codebase(

































        return filenames_and_contents

    def _repo_to_files_and_token_lengths(
        self,
        repo_tree: git.Repo,
        excluded_files: list[str] = None,
    ) -> list[tuple[str, int]]:
        files_with_token_lengths = []
        for blob in repo_tree.traverse():
            if blob.type == 'tree':
                continue
            if excluded_files is not None and blob.path in excluded_files:
                continue
            content = blob.data_stream.read().decode()
            token_length = len(self.rail_service.tokenizer.encode(content))
            files_with_token_lengths.append((blob.path, token_length))
        return files_with_token_lengths

    def create_gptignore(self):
        gptignore_path = Path('.gptignore')
        if not gptignore_path.exists():
            with gptignore_path.open('w') as gptignore_file:
                gptignore_file.write('*.lock

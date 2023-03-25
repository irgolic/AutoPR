







from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \
    Diff, CommitPlan
from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \
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

    @staticmethod
    def repo_to_codebase(

































        return filenames_and_contents

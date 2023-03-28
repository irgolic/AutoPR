from typing import Optional

from git.repo import Repo

from autopr.models.artifacts import DiffStr, Issue
from autopr.models.rail_objects import PullRequestDescription, CommitPlan, Diff
from autopr.models.rails import NewDiff, FileDescriptor
from autopr.services.codegen_service import CodegenServiceBase

import structlog

from autopr.utils.repo import repo_to_file_descriptors

log = structlog.get_logger()


class RailCodegenService(CodegenServiceBase):
    id = "rail-v1"

    def __init__(
        self,
        *args,
        file_context_token_limit: int = 5000,
        file_chunk_size: int = 500,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.file_context_token_limit = file_context_token_limit
        self.file_chunk_size = file_chunk_size

    def _generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> DiffStr:
        # Get files
        files = repo_to_file_descriptors(repo, self.file_context_token_limit, self.file_chunk_size)

        # Serialize issue
        issue_text = issue.to_str()
        
        # Serialize pull request description
        pr_text_description = pr_desc.to_str()

        # Serialize current commit
        commit_description = current_commit.to_str()

        # Grab relevant files
        relevant_filepaths = [f for f in current_commit.relevant_filepaths]
        files_subset = []
        for f in files:
            if f.path in relevant_filepaths:
                files_subset.append(f.copy(deep=True))

        # If any files are not found, see if they are a stem of a file in the repo
        subset_paths = [f.path for f in files_subset]
        fps_not_found = [
            fp for fp in relevant_filepaths
            if fp not in subset_paths
        ]
        for fp in fps_not_found:
            for f in files:
                if f.path.endswith(fp) and f.path not in subset_paths:
                    files_subset.append(f.copy(deep=True))
                    break

        log.debug('Files to look at:')
        for f in files_subset:
            log.debug(f' - {f.path}')

        # Run NewDiff rail
        rail = NewDiff(
            issue=issue_text,
            pull_request_description=pr_text_description,
            selected_file_contents=files_subset,
            commit=commit_description,
        )
        patch = self.rail_service.run_rail(rail)
        if patch is None or not isinstance(patch, Diff):
            raise ValueError('Error generating patch')
        patch_text = patch.diff or ''

        # if not all chunks were looked at, keep running the rail until all chunks are looked at
        not_looked_at_files = []

        def update_not_looked_at_files():
            nonlocal not_looked_at_files

            not_looked_at_files = []
            for f in files_subset:
                if f.end_chunk == len(f.chunks):
                    continue
                f.start_chunk = f.end_chunk
                f.end_chunk = len(f.chunks)
                not_looked_at_files.append(f)

        update_not_looked_at_files()
        reasks = self.rail_service.num_reasks
        while not_looked_at_files and reasks > 0:
            reasks -= 1
            log.debug(f'Generating patch over more code... ({reasks} reasks left)')

            for f in not_looked_at_files:
                log.debug(f' - {f.path} ({f.end_chunk - f.start_chunk} chunks left)')

            files_subset = [
                f.copy(deep=True) for f in files_subset
                if f.end_chunk != len(f.chunks)
            ]
            rail = NewDiff(
                issue=issue_text,
                pull_request_description=pr_text_description,
                selected_file_contents=not_looked_at_files,
                commit=commit_description,
            )
            patch = self.rail_service.run_rail(rail)
            if patch is None or not isinstance(patch, Diff):
                raise ValueError('Error generating patch')
            patch_text += patch.diff or ''
            update_not_looked_at_files()

        return patch_text

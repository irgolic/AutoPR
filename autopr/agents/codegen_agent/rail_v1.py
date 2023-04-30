from typing import Optional

from git.repo import Repo

from autopr.models.artifacts import DiffStr, Issue
from autopr.models.rail_objects import PullRequestDescription, CommitPlan, RailObject
from autopr.models.prompt_rails import PromptRail
from .base import CodegenAgentBase

import structlog

from autopr.utils.repo import repo_to_file_descriptors, trim_chunk, FileDescriptor

log = structlog.get_logger()


class Diff(RailObject):
    output_spec = """<string
    name="diff"
    description="The diff of the commit, in unified format (unidiff), as output by `diff -u`. Changes shown in hunk format, with headers akin to `--- filename\n+++ filename\n@@ .,. @@`."
    required="false"
    format="unidiff"
/>"""

    diff: Optional[DiffStr] = None


class Commit(RailObject):
    # TODO use this instead of Diff, to get a commit message rewrite
    #  EDIT: development focus has shifted to the autonomous codegen agent as a better solution
    output_spec = f"""{Diff.output_spec}
<string
    name="message"
    description="The commit message, describing the changes."
    required="true"
    format="length: 5 72"
    on-fail-length="noop"
/>"""

    diff: Diff
    commit_message: str


class NewDiff(PromptRail):
    # Generate code for a commit, given an issue, a pull request, and a codebase
    prompt_spec = f"""Hey, now that we've got a plan, let's write some code.

This is the issue that was opened:
```{{issue}}```

This is the plan to address it:
```{{pull_request_description}}```

This is the codebase subset we decided to look at:
```{{codebase}}```

This is the commit for which we're writing a unidiff:
```{{commit}}```

Please implement the commit, and send me the unidiff. 
Only write a unidiff in the codebase subset we're looking at."""

    output_type = Diff
    extra_params = {
        'temperature': 0.0,
    }

    issue: Issue
    pull_request_description: PullRequestDescription
    selected_file_contents: list[FileDescriptor]
    commit: CommitPlan

    def get_string_params(self) -> dict[str, str]:
        return {
            'issue': str(self.issue),
            'pull_request_description': str(self.pull_request_description),
            'codebase': '\n'.join([
                file_descriptor.filenames_and_contents_to_str()
                for file_descriptor in self.selected_file_contents
            ]),
            'commit': str(self.commit),
        }

    def trim_params(self) -> bool:
        return trim_chunk(self.selected_file_contents)


class RailCodegenAgent(CodegenAgentBase):
    """
    Generate and apply diff given a CommitPlan.
    It chunkifies the files specified in CommitPlan.relevant_file_hunks,
    and writes diffs as it goes along looking at the file chunks.

    WARNING: This agent implementation heavily relies on the `unidiff` custom guardrails validator,
    and it still sometimes produces ambiguous results.
    If you're interested in continuing experimentation with the diff generation approach,
    try few-shotting. At time of writing, few-shotting is not implemented in guardrails.

    Parameters
    ----------

    file_context_token_limit: int
        The maximum size taken up by the file context (concatenated file chunks) in the prompt.

    file_chunk_size: int
        The maximum token size of each chunk that a file is split into.
    """

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

    def _generate_changes(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> None:
        # Get files
        files = repo_to_file_descriptors(repo, self.file_context_token_limit, self.file_chunk_size)

        # Grab relevant files
        relevant_filepaths = [f.filepath for f in current_commit.relevant_file_hunks]
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
            issue=issue,
            pull_request_description=pr_desc,
            selected_file_contents=files_subset,
            commit=current_commit,
        )
        patch = self.rail_service.run_prompt_rail(rail)
        if patch is None or not isinstance(patch, Diff):
            raise ValueError('Error generating patch')
        patch_text = patch.diff or ''

        # If not all chunks were looked at, keep running the rail until all chunks are looked at
        not_looked_at_files = []

        def update_not_looked_at_files():
            """
            Update the list of files to look at in the next iteration.
            """
            nonlocal not_looked_at_files

            not_looked_at_files = []
            for f in files_subset:
                if f.end_chunk == len(f.chunks):
                    continue
                f.start_chunk = f.end_chunk
                f.end_chunk = len(f.chunks)
                not_looked_at_files.append(f)

        update_not_looked_at_files()

        # If there are still files to look at, keep running the rail and generating patches
        reasks = self.rail_service.num_reasks
        while not_looked_at_files and reasks > 0:
            reasks -= 1
            log.debug(f'Generating patch over more code... ({reasks} reasks left)')

            for f in not_looked_at_files:
                log.debug(f' - {f.path} ({f.end_chunk - f.start_chunk} chunks left)')

            # Only look at the files that haven't been looked at yet
            files_subset = [
                f.copy(deep=True) for f in files_subset
                if f.end_chunk != len(f.chunks)
            ]
            # Run NewDiff rail
            rail = NewDiff(
                issue=issue,
                pull_request_description=pr_desc,
                selected_file_contents=not_looked_at_files,
                commit=current_commit,
            )
            patch = self.rail_service.run_prompt_rail(rail)
            if patch is None or not isinstance(patch, Diff):
                raise ValueError('Error generating patch')

            # Concatenate the patch text
            patch_text += patch.diff or ''
            update_not_looked_at_files()

        # Apply patch
        self.diff_service.apply_diff(patch_text)

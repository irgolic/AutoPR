import tempfile
from typing import Callable

import git
import pydantic
import transformers
from git import Tree

from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse, \
    Diff, CommitPlan
from autopr.models.rails import InitialFileSelectRail, ContinueLookingAtFiles, LookAtFiles, ProposePullRequest, \
    NewDiff, FileDescriptor
from autopr.models.repo import RepoCommit
from autopr.models.repo import RepoPullRequest
from autopr.services.rail_service import RailService

import structlog
log = structlog.get_logger()


class GenerationService:
    def __init__(
        self,
        rail_service: RailService,
        file_context_token_limit: int = 5000,
        file_chunk_size: int = 512,
    ):
        self.rail_service = rail_service
        self.file_context_token_limit = file_context_token_limit
        self.file_chunk_size = file_chunk_size
        self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=8192)

    @staticmethod
    def repo_to_codebase(
        tree: Tree,
        included_filepaths: list[str] = None,
        excluded_filepaths: list[str] = None,
    ) -> list[tuple[str, str]]:
        # Concatenate all the files in the repo,

        filenames_and_contents = []
        for blob in tree.traverse():
            if included_filepaths is not None and blob.path not in included_filepaths:
                continue
            if excluded_filepaths is not None and blob.path in excluded_filepaths:
                continue

            # Skip directories
            if blob.type == 'tree':
                continue

            # Skip lock file
            if any(
                blob.path.endswith(ending)
                for ending in ['.lock']
            ):
                continue

            # Add file contents, with line numbers
            blob_text = blob.data_stream.read().decode()
            blob_contents_with_line_numbers = ""
            for i, line in enumerate(blob_text.split('\n')):
                blob_contents_with_line_numbers += f"{i+1} {line}\n"

            filenames_and_contents += [(blob.path, blob_contents_with_line_numbers)]

        return filenames_and_contents

    def _repo_to_files_and_token_lengths(
        self,
        repo_tree: Tree,
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

    def _repo_to_file_descriptors(self, repo_tree: Tree) -> list[FileDescriptor]:
        file_descriptor_list = []
        for blob in repo_tree.traverse():
            if blob.type == 'tree':
                continue
            content = blob.data_stream.read().decode()
            tokens = self.tokenizer.encode(content)

            # Split into chunks up to the last newline
            chunks: list[list[tuple[int, str]]] = []
            line_buffer = []
            for i, line in enumerate(content.splitlines()):
                line_buffer.append((i, line))
                # FIXME speed this up
                token_length = len(self.tokenizer.encode(
                    '\n'.join([l[1] for l in line_buffer])
                ))
                if token_length >= self.file_chunk_size:
                    chunks.append(line_buffer)
                    line_buffer = []
            if line_buffer:
                chunks.append(line_buffer)

            token_length = len(tokens)
            file_descriptor_list.append(FileDescriptor(
                path=blob.path,
                token_length=token_length,
                chunks=chunks,
            ))
        return file_descriptor_list

    def get_initial_filepaths(self, files: list[FileDescriptor], issue_text: str) -> list[str]:
        log.debug('Getting filepaths to look at...')

        response: InitialFileSelectResponse = self.rail_service.run_rail(
            InitialFileSelectRail(
                issue=issue_text,
                file_descriptors=files,
                token_limit=self.file_context_token_limit
            )
        )
        if response is None:
            real_filepaths = []
        else:
            real_filepaths = [fp for fp in response.filepaths if fp is not None]
            if len(response.filepaths) != len(real_filepaths):
                log.debug(f'Got hallucinated filepaths: {set(response.filepaths) - set(real_filepaths)}')
            if real_filepaths:
                log.debug(f'Got filepaths:')
                for filepath in real_filepaths:
                    log.debug(f' -  {filepath}')

        return real_filepaths

    def write_notes_about_files(self, files: list[FileDescriptor], issue_text: str, filepaths: list[str]) -> str:
        log.debug('Looking at files...')

        file_contents = [
            f.copy(deep=True) for f in files
            if f.path in filepaths
        ]
        rail = LookAtFiles(
            issue=issue_text,
            selected_file_contents=file_contents,
            prospective_file_descriptors=[f.copy(deep=True) for f in files],
            token_limit=self.file_context_token_limit,
        )
        response: LookAtFilesResponse = self.rail_service.run_rail(rail)
        if response is None:
            raise ValueError('Error looking at files')
        filepaths = response.filepaths_we_should_look_at
        notes = response.notes

        viewed_filepaths_up_to_chunk: dict[str, int] = {}
        reasks = self.rail_service.num_reasks
        while filepaths and reasks > 0:
            reasks -= 1

            log.debug(f'Looking at more files... ({reasks} reasks left)')
            for fp in filepaths:
                log.debug(f' - {fp}')

            for fp in rail.selected_file_contents:
                viewed_filepaths_up_to_chunk[fp.path] = fp.end_chunk
            file_contents = []
            for f in files:
                if f.path not in filepaths:
                    continue
                if f.path in viewed_filepaths_up_to_chunk:
                    chunk_num = viewed_filepaths_up_to_chunk[f.path]
                    if chunk_num == f.end_chunk:
                        continue
                    new_f = f.copy(deep=True)
                    new_f.start_chunk = chunk_num
                else:
                    new_f = f.copy(deep=True)
                file_contents.append(new_f)
            rail = ContinueLookingAtFiles(
                issue=issue_text,
                notes=notes,
                selected_file_contents=file_contents,
                prospective_file_descriptors=rail._filtered_prospective_file_descriptors,
                token_limit=self.file_context_token_limit,
            )
            response: LookAtFilesResponse = self.rail_service.run_rail(rail)
            if response is None:
                filepaths = []
            else:
                filepaths = response.filepaths_we_should_look_at
                notes += f'\n{response.notes}'

        return notes

    def propose_pull_request(self, issue_text: str, notes: str) -> PullRequestDescription:
        log.debug('Getting commit messages...')
        pr_desc: PullRequestDescription = self.rail_service.run_rail(
            ProposePullRequest(
                issue=issue_text,
                notes_taken_while_looking_at_files=notes,
            )
        )
        if pr_desc is None:
            raise ValueError('Error proposing pull request')
        return pr_desc

    def generate_patch(
        self,
        files: list[FileDescriptor],
        issue_text: str,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan
    ) -> str:
        log.debug('Generating patch...')
        pr_text_description = f"Title: {pr_desc.title}\n\n{pr_desc.body}\n\n"
        for i, commit_plan in enumerate(pr_desc.commits):
            prefix = f" {' ' * len(str(i + 1))}  "
            changes_prefix = f"\n{prefix}  "
            pr_text_description += (
                f"{str(i + 1)}. Commit: {commit_plan.commit_message}\n"
                f"{prefix}Files: {','.join(commit_plan.relevant_filepaths)}\n"
                f"{prefix}Changes:"
                f"{changes_prefix}{changes_prefix.join(commit_plan.commit_changes_description.splitlines())}\n"
            )

        files_subset = []
        for f in files:
            if f.path in current_commit.relevant_filepaths:
                files_subset.append(f.copy(deep=True))
        # If any files are not found, see if they are a stem of a file in the repo
        subset_paths = [f.path for f in files_subset]
        fps_not_found = [
            fp for fp in current_commit.relevant_filepaths
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

        commit_description = current_commit.commit_message + '\n\n' + current_commit.commit_changes_description

        rail = NewDiff(
            issue=issue_text,
            pull_request_description=pr_text_description,
            selected_file_contents=files_subset,
            commit=commit_description,
        )
        patch: Diff = self.rail_service.run_rail(rail)
        if patch is None:
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
            patch: Diff = self.rail_service.run_rail(rail)
            if patch is None:
                raise ValueError('Error generating patch')
            patch_text += patch.diff or ''
            update_not_looked_at_files()

        return patch_text

    def generate_pr(
        self,
        repo: git.Repo,
        issue_title: str,
        issue_body: str,
        issue_number: int,
        handle_commit: Callable[[PullRequestDescription, RepoCommit], None]
    ) -> RepoPullRequest:
        issue_text = f"Issue #{str(issue_number)}\nTitle: {issue_title}\n\n{issue_body}"

        # Get file descriptors from repo
        repo_tree = repo.head.commit.tree
        files = self._repo_to_file_descriptors(repo_tree)

        # Get the filepaths to look at
        filepaths = self.get_initial_filepaths(files, issue_text)

        if filepaths:
            # Look at the files
            notes = self.write_notes_about_files(files, issue_text, filepaths)
        else:
            notes = "The repository's contents were irrelevant, only create new files to address the issue."

        # Get the commit messages and relevant filepaths
        pr_desc = self.propose_pull_request(issue_text, notes)

        # Generate the patch
        commits = []
        for commit_plan in pr_desc.commits:
            diff = self.generate_patch(
                files,
                issue_text,
                pr_desc,
                commit_plan
            )
            repo_commit = RepoCommit(
                message=commit_plan.commit_message,
                diff=diff,
            )
            handle_commit(pr_desc, repo_commit)
            repo_tree = repo.head.commit.tree
            files = self._repo_to_file_descriptors(repo_tree)

        pr_model = RepoPullRequest(
            title=pr_desc.title,
            body=pr_desc.body,
            commits=commits,
        )

        # Print the PR
        print(f"""PR title: {pr_model.title}

{pr_model.body}

Commits:""")
        for commit in pr_model.commits:
            print(f""" - {commit.message}

{commit.diff}\n\n""")

        return pr_model

from git.repo import Repo

from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription, InitialFileSelectResponse, LookAtFilesResponse
from autopr.models.rails import ProposePullRequest, FileDescriptor, InitialFileSelectRail, LookAtFiles, \
    ContinueLookingAtFiles
from autopr.services.planner_service.base import PlannerServiceBase
from autopr.utils.repo import repo_to_file_descriptors


class RailPlannerService(PlannerServiceBase):
    id = 'rail-v1'

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

    def get_initial_filepaths(
        self,
        files: list[FileDescriptor],
        issue_text: str,
    ) -> list[str]:
        self.log.debug('Getting filepaths to look at...')

        response = self.rail_service.run_rail(
            InitialFileSelectRail(
                issue=issue_text,
                file_descriptors=files,
                token_limit=self.file_context_token_limit
            )
        )
        if response is None or not isinstance(response, InitialFileSelectResponse):
            real_filepaths = []
        else:
            real_filepaths = [fp for fp in response.filepaths if fp is not None]
            if len(response.filepaths) != len(real_filepaths):
                self.log.debug(f'Got hallucinated filepaths: {set(response.filepaths) - set(real_filepaths)}')
            if real_filepaths:
                self.log.debug(f'Got filepaths:')
                for filepath in real_filepaths:
                    self.log.debug(f' -  {filepath}')

        return real_filepaths

    def write_notes_about_files(self, files: list[FileDescriptor], issue_text: str, filepaths: list[str]) -> str:
        self.log.debug('Looking at files...')

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
        response = self.rail_service.run_rail(rail)
        if response is None or not isinstance(response, LookAtFilesResponse):
            raise ValueError('Error looking at files')
        filepaths = response.filepaths_we_should_look_at or []
        notes = response.notes

        viewed_filepaths_up_to_chunk: dict[str, int] = {}
        reasks = self.rail_service.num_reasks
        while filepaths and reasks > 0:
            reasks -= 1

            # See if all requested files have already been viewed
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

            if not file_contents:
                break

            self.log.debug(f'Looking at more files... ({reasks} reasks left)')
            for fp in filepaths:
                self.log.debug(f' - {fp}')

            rail = ContinueLookingAtFiles(
                issue=issue_text,
                notes=notes,
                selected_file_contents=file_contents,
                prospective_file_descriptors=rail._filtered_prospective_file_descriptors,
                token_limit=self.file_context_token_limit,
            )
            response = self.rail_service.run_rail(rail)
            if response is None or not isinstance(response, LookAtFilesResponse):
                filepaths = []
            else:
                filepaths = response.filepaths_we_should_look_at or []
                notes += f'\n{response.notes}'

        return notes

    def propose_pull_request(self, issue_text: str, notes: str) -> PullRequestDescription:
        self.log.debug('Getting commit messages...')
        pr_desc = self.rail_service.run_rail(
            ProposePullRequest(
                issue=issue_text,
                notes_taken_while_looking_at_files=notes,
            )
        )
        if pr_desc is None or not isinstance(pr_desc, PullRequestDescription):
            raise ValueError('Error proposing pull request')
        return pr_desc

    def _plan_pr(
        self,
        repo: Repo,
        issue: Issue,
    ) -> PullRequestDescription:
        # Get files
        files = repo_to_file_descriptors(repo, self.file_context_token_limit, self.file_chunk_size)

        # Serialize issue
        issue_text = issue.to_str()

        # Get the filepaths to look at
        filepaths = self.get_initial_filepaths(files, issue_text)

        if filepaths:
            # Look at the files
            notes = self.write_notes_about_files(files, issue_text, filepaths)
        else:
            notes = "The repository's contents were irrelevant, only create new files to address the issue."

        return self.propose_pull_request(issue_text, notes)

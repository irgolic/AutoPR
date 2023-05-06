from typing import Union, Optional

import pydantic
from git.repo import Repo

from autopr.models.artifacts import Issue
from autopr.models.events import EventUnion
from autopr.models.rail_objects import PullRequestDescription, RailObject
from autopr.models.prompt_rails import PromptRail
from .base import PullRequestAgentBase
from autopr.utils.repo import repo_to_file_descriptors, trim_chunk, filter_seen_chunks, FileDescriptor


class InitialFileSelectResponse(RailObject):
    output_spec = """<list name="filepaths">
    <string
        description="Files in this repository that we should look at."
    />
</list>"""

    filepaths: list[str]

    @classmethod
    def get_rail_spec(cls):
        return f"""
<rail version="0.1">
<output>
{cls.output_spec}
</output>
<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

@json_suffix_prompt_examples
</instructions>
<prompt>
Given the following document surrounded by `+++++`, answer the following questions. 
If the answer doesn't exist in the document, enter `null`.

+++++
{{{{raw_document}}}}
+++++

Extract information from this document and return a JSON that follows the correct schema.
If looking at files would be a waste of time, please submit an empty list.

@xml_prefix_prompt

{{output_schema}}
</prompt>
</rail>
"""

class InitialFileSelect(PromptRail):
    # Select files given issue and files in repo
    prompt_template = f"""Hey, somebody just opened an issue in my repo, could you help me write a pull request?

The issue is:
```{{issue}}```

The list of files in the repo is:
```{{filepaths_with_token_lengths}}```

Should we take a look at any files? If so, pick only a few files (max {{token_limit}} tokens). 
Respond with a very short rationale, and a list of files.
If looking at files would be a waste of time with regard to the issue, respond with an empty list."""

    output_type = InitialFileSelectResponse
    # extra_params = {
    #     'temperature': 0,
    # }

    issue: Issue
    file_descriptors: list[FileDescriptor]
    token_limit: int

    def get_string_params(self) -> dict[str, str]:
        return {
            'issue': str(self.issue),
            'filepaths_with_token_lengths': '\n'.join([
                file_descriptor.filepaths_with_token_lengths_to_str()
                for file_descriptor in self.file_descriptors
            ]),
            'token_limit': str(self.token_limit),
        }


class LookAtFilesResponse(RailObject):
    output_spec = """<string 
    name="notes" 
    description="Notes relevant to solving the issue, that we will use to plan our code commits." 
    length="1 1000"
    on-fail="noop" 
/>
<list name="filepaths_we_should_look_at">
    <string
        description="The paths to files we should look at next in the repo. Drop any files that are a waste of time with regard to the issue."
    />
</list>"""

    filepaths_we_should_look_at: Optional[list[str]] = None
    notes: str

    @classmethod
    def get_rail_spec(cls):
        return f"""
<rail version="0.1">
<output>
{cls.output_spec}
</output>
<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

@json_suffix_prompt_examples
</instructions>
<prompt>
Given the following document surrounded by `+++++`, answer the following questions. 
If the answer doesn't exist in the document, enter `null`.

+++++
{{{{raw_document}}}}
+++++

Extract information from this document and return a JSON that follows the correct schema.
If looking at files would be a waste of time, please submit an empty list.

@xml_prefix_prompt

{{output_schema}}
</prompt>
</rail>
"""



class LookAtFiles(PromptRail):
    # Select files given issue, unseen files in repo, and notes
    prompt_template = f"""Hey, somebody just submitted an issue, could you own it, and write a pull request?

The issue that was opened:
```{{issue}}```

We've decided to look at these files:
```{{codebase}}```

The list of files in the repo that we haven't taken a look at yet:
```{{filepaths_with_token_lengths}}```

Take some notes that will help us plan our code commits, in an effort to close the issue. 
Also, should we take a look at any other files? If so, pick only a few files (max {{token_limit}} tokens).
Respond with some very brief notes, and a list of files to continue looking at. 
If looking at files would be a waste of time with regard to the issue, respond with an empty list."""

    output_type = LookAtFilesResponse
    # extra_params = {
    #     'temperature': 0.2,
    # }

    issue: Issue
    selected_file_contents: list[FileDescriptor]
    prospective_file_descriptors: list[FileDescriptor]
    token_limit: int
    _filtered_prospective_file_descriptors: list[FileDescriptor] = pydantic.PrivateAttr(default_factory=list)

    def get_string_params(self) -> dict[str, str]:
        self._filtered_prospective_file_descriptors = filter_seen_chunks(
            self.selected_file_contents, self.prospective_file_descriptors
        )

        return {
            'issue': str(self.issue),
            'codebase': '\n'.join([
                file_descriptor.filenames_and_contents_to_str()
                for file_descriptor in self.selected_file_contents
            ]),
            'filepaths_with_token_lengths': '\n'.join([
                file_descriptor.filepaths_with_token_lengths_to_str()
                for file_descriptor in self._filtered_prospective_file_descriptors
            ]),
            'token_limit': str(self.token_limit),
        }

    def trim_params(self) -> bool:
        return trim_chunk(self.selected_file_contents)


class ContinueLookingAtFiles(PromptRail):
    # Continue selecting files and generating fp_notes given issue, unseen files in repo, and notes
    prompt_template = f"""Hey, somebody just submitted an issue, could you own it, and write a pull request?

The issue that was opened:
```{{issue}}```

Some notes we've taken while looking at files so far:
```{{notes}}```

We've decided to look at these files:
```{{codebase}}```

The list of files in the repo that we haven't taken a look at yet:
```{{filepaths_with_token_lengths}}```

Take some notes that will help us plan commits and write code to fix the issue. 
Also, let me know if we should take a look at any other files – our budget is {{token_limit}} tokens."""

    output_type = LookAtFilesResponse
    # extra_params = {
    #     'temperature': 0.2,
    # }

    issue: Issue
    notes: str
    selected_file_contents: list[FileDescriptor]
    prospective_file_descriptors: list[FileDescriptor]
    token_limit: int
    _filtered_prospective_file_descriptors: list[FileDescriptor] = pydantic.PrivateAttr(default_factory=list)

    def get_string_params(self) -> dict[str, str]:
        self._filtered_prospective_file_descriptors = filter_seen_chunks(
            self.selected_file_contents, self.prospective_file_descriptors
        )

        return {
            'issue': str(self.issue),
            'notes': self.notes,
            'codebase': '\n'.join([
                file_descriptor.filenames_and_contents_to_str()
                for file_descriptor in self.selected_file_contents
            ]),
            'filepaths_with_token_lengths': '\n'.join([
                file_descriptor.filepaths_with_token_lengths_to_str()
                for file_descriptor in self._filtered_prospective_file_descriptors
            ]),
            'token_limit': str(self.token_limit),
        }

    def trim_params(self) -> bool:
        return trim_chunk(self.selected_file_contents)


class ProposePullRequest(PromptRail):
    # Generate proposed list of commit messages, given notes and issue
    prompt_template = f"""Hey somebody just submitted an issue, could you own it, write some commits, and a pull request?

These are notes we took while looking at the repo:
```{{notes_taken_while_looking_at_files}}```

This is the issue that was opened:
```{{issue}}```

When you're done, send me the pull request title, body, and a list of commits, each coupled with which files we should be looking at to write the commit's code.
Ensure you specify the files relevant to the commit, especially if the commit is a refactor.
Folders are created automatically; do not make them in their own commit."""

    output_type = PullRequestDescription
    # extra_params = {
    #     'temperature': 0.1,
    # }

    notes_taken_while_looking_at_files: str
    issue: Issue


class RailPullRequestAgent(PullRequestAgentBase):
    """
    Plan a pull request by iteratively selecting files to look at, taking notes while looking at them,
    and then generating a list of commits.

    File selection is performed by giving the agent a list of filenames, and asking it to select a subset of them.

    Parameters
    ----------
    file_context_token_limit: int
        The maximum size taken up by the file context (concatenated file chunks) in the prompt.

    file_chunk_size: int
        The maximum token size of each chunk that a file is split into.
    """

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
        issue: Issue,
    ) -> list[str]:
        self.log.debug('Getting filepaths to look at...')

        response = self.rail_service.run_prompt_rail(
            InitialFileSelect(
                issue=issue,
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

    def write_notes_about_files(
        self,
        files: list[FileDescriptor],
        issue: Issue,
        filepaths: list[str]
    ) -> str:
        self.log.debug('Looking at files...')

        file_contents = [
            f.copy(deep=True) for f in files
            if f.path in filepaths
        ]
        rail = LookAtFiles(
            issue=issue,
            selected_file_contents=file_contents,
            prospective_file_descriptors=[f.copy(deep=True) for f in files],
            token_limit=self.file_context_token_limit,
        )
        response = self.rail_service.run_prompt_rail(rail)
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
                issue=issue,
                notes=notes,
                selected_file_contents=file_contents,
                prospective_file_descriptors=rail._filtered_prospective_file_descriptors,
                token_limit=self.file_context_token_limit,
            )
            response = self.rail_service.run_prompt_rail(rail)
            if response is None or not isinstance(response, LookAtFilesResponse):
                filepaths = []
            else:
                filepaths = response.filepaths_we_should_look_at or []
                notes += f'\n{response.notes}'

        return notes

    def propose_pull_request(self, issue: Issue, notes: str) -> PullRequestDescription:
        self.log.debug('Getting commit messages...')
        pr_desc = self.rail_service.run_prompt_rail(
            ProposePullRequest(
                issue=issue,
                notes_taken_while_looking_at_files=notes,
            )
        )
        if pr_desc is None or not isinstance(pr_desc, PullRequestDescription):
            raise ValueError('Error proposing pull request')
        return pr_desc

    def _plan_pull_request(
        self,
        repo: Repo,
        issue: Issue,
        event: EventUnion,
    ) -> Union[str, PullRequestDescription]:
        # Get files
        files = repo_to_file_descriptors(repo, self.file_context_token_limit, self.file_chunk_size)

        # Get the filepaths to look at
        filepaths = self.get_initial_filepaths(files, issue)

        if filepaths:
            # Look at the files
            notes = self.write_notes_about_files(files, issue, filepaths)
        else:
            notes = "The repository's contents were irrelevant, only create new files to address the issue."

        return self.propose_pull_request(issue, notes)

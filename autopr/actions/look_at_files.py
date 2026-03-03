from typing import Union, Optional

import pydantic
from git.repo import Repo

from autopr.actions.base import Action, ContextDict
from autopr.actions.utils.commit import PullRequestDescription
from autopr.models.artifacts import Issue
from autopr.models.prompt_rails import PromptRail
from autopr.models.rail_objects import RailObject
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

{{context}}

The list of files in the repo is:
```{{filepaths_with_token_lengths}}```

Should we take a look at any files? If so, pick only a few files (max {{token_limit}} tokens). 
Respond with a very short rationale, and a list of files.
If looking at files would be a waste of time with regard to the issue, respond with an empty list."""

    output_type = InitialFileSelectResponse
    # extra_params = {
    #     'temperature': 0,
    # }

    context: ContextDict
    file_descriptors: list[FileDescriptor]
    token_limit: int

    def get_string_params(self) -> dict[str, str]:
        return {
            'context': str(self.context),
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

{{context}}

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

    context: ContextDict
    selected_file_contents: list[FileDescriptor]
    prospective_file_descriptors: list[FileDescriptor]
    token_limit: int
    _filtered_prospective_file_descriptors: list[FileDescriptor] = pydantic.PrivateAttr(default_factory=list)

    def get_string_params(self) -> dict[str, str]:
        self._filtered_prospective_file_descriptors = filter_seen_chunks(
            self.selected_file_contents, self.prospective_file_descriptors
        )

        return {
            'context': str(self.context),
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
        if trim_chunk(self.selected_file_contents):
            return True
        return super().trim_params()


class ContinueLookingAtFiles(PromptRail):
    # Continue selecting files and generating fp_notes given issue, unseen files in repo, and notes
    prompt_template = f"""Hey, somebody just submitted an issue, could you own it, and write a pull request?

{{context}}

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

    context: ContextDict
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
            'context': str(self.context),
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
        if trim_chunk(self.selected_file_contents):
            return True
        return super().trim_params()


class InspectFiles(Action):
    """
    Iteratively select files to look at, taking notes while looking at them.

    File selection is performed by giving the agent a list of filenames, and asking it to select a subset of them.

    Parameters
    ----------
    file_context_token_limit: int
        The maximum size taken up by the file context (concatenated file chunks) in the prompt.

    file_chunk_size: int
        The maximum token size of each chunk that a file is split into.
    """

    id = 'look_at_files'

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
        context: ContextDict,
    ) -> list[str]:
        self.log.debug('Getting filepaths to look at...')

        response = self.rail_service.run_prompt_rail(
            InitialFileSelect(
                context=context,
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
        context: ContextDict,
        filepaths: list[str]
    ) -> str:
        self.log.debug('Looking at files...')

        file_contents = [
            f.copy(deep=True) for f in files
            if f.path in filepaths
        ]
        rail = LookAtFiles(
            context=context,
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
                context=context,
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

    def run(
        self,
        args: Action.Arguments,
        context: ContextDict,
    ) -> ContextDict:
        self.publish_service.update_section("📖 Looking at files")

        # Get files
        files = repo_to_file_descriptors(self.repo, self.file_context_token_limit, self.file_chunk_size)

        # Get the filepaths to look at
        filepaths = self.get_initial_filepaths(files, context)

        if filepaths:
            # Look at the files
            notes = self.write_notes_about_files(files, context, filepaths)
        else:
            notes = "The repository's contents were irrelevant, only create new files to address the issue."

        context['notes'] = notes

        self.publish_service.update_section("📖 Looked at files")
        return context

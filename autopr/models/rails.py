from typing import ClassVar, Union, Optional, Any

import pydantic
from pydantic import root_validator

from autopr.models.rail_objects import LookAtFilesResponse, PullRequestDescription, \
    InitialFileSelectResponse, RailObject, Diff

import structlog
log = structlog.get_logger()


class Rail(pydantic.BaseModel):
    prompt_spec: ClassVar[str] = ''
    output_type: ClassVar[RailObject] = ...
    extra_params: ClassVar[dict[str, Any]] = {}

    def get_string_params(self) -> dict[str, str]:
        prompt_params = dict(self)
        if any(not isinstance(value, str) for value in prompt_params.values()):
            raise NotImplementedError
        return prompt_params

    def trim_params(self) -> bool:
        log.warning("Naively trimming params", rail=self)
        prompt_params = dict(self)
        # If there are any lists, remove the last element of the first one you find
        for key, value in prompt_params.items():
            if isinstance(value, list) and len(value) > 0:
                setattr(self, key, value[:-1])
                return True
        return False

    @classmethod
    def get_rail_spec(cls):
        return f"""
<rail version="0.1">
<output>
{cls.output_type.rail_spec}
</output>
<prompt>
```
{{{{raw_response}}}}
```

@xml_prefix_prompt

{{output_schema}}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""


class FileDescriptor(pydantic.BaseModel):
    path: str
    token_length: int
    chunks: list[list[tuple[int, str]]]  # list of (line number, line content) pairs
    start_chunk: int = 0
    end_chunk: Optional[int]

    @root_validator(pre=True)
    def validate_end_chunk(cls, values):
        if 'end_chunk' not in values:
            values['end_chunk'] = len(values['chunks'])
        return values

    def filepaths_with_token_lengths_to_str(self) -> str:
        # TODO give info on what chunks we've already seen
        return f'{self.path} ({str(self.token_length)} tokens)'
        # chunks_left = self.end_chunk - self.start_chunk
        # return f'{self.path} ({str(self.token_length)} tokens) ({str(chunks_left)} chunks left)'

    def filenames_and_contents_to_str(self) -> str:
        contents = ''
        if self.start_chunk > 0:
            contents += f'... #  (omitting {self.start_chunk} chunks)\n'
        # TODO make the line numbers right-aligned with padded spaces,
        #  so that the line numbers don't change the start of the line
        contents += '\n'.join([
            f'{str(line_number)} {line_content}'
            for chunk in self.chunks[self.start_chunk:self.end_chunk]
            for line_number, line_content in chunk
        ])
        if self.end_chunk < len(self.chunks):
            contents += f'\n... #  (omitting {len(self.chunks) - self.end_chunk} chunks)'
        return f'>>> Path: {self.path}:\n\n{contents}'


def _trim_chunk(file_desc_with_chunk_start_end: list[FileDescriptor]) -> bool:
    if file_desc_with_chunk_start_end:
        # Find file with most chunks
        longest_num = 0
        longest_i = 0
        for i, desc in enumerate(file_desc_with_chunk_start_end):
            num_chunks = desc.end_chunk - desc.start_chunk
            if num_chunks > longest_num:
                longest_num = num_chunks
                longest_i = i

        desc = file_desc_with_chunk_start_end[longest_i]

        # If we've already looked at the whole file, remove it from the list
        if desc.start_chunk == desc.end_chunk - 1:
            del file_desc_with_chunk_start_end[longest_i]
            return True

        # Otherwise, shave a chunk off the end
        desc.end_chunk -= 1
        file_desc_with_chunk_start_end[longest_i] = desc
        return True
    return False


def _filter_seen_chunks(seen_fds: list[FileDescriptor], prospective_fds: list[FileDescriptor]) -> list[FileDescriptor]:
    fds_copy = [f.copy(deep=True) for f in prospective_fds]
    omit_prospective_fd_indices = []
    for selected_fd in seen_fds:
        # If it's in prospective_file_descriptors, update its start_chunk
        for prospective_fd in fds_copy:
            if prospective_fd.path == selected_fd.path:
                # If we've already looked at the whole file, remove it from the list
                if prospective_fd.end_chunk == selected_fd.end_chunk:
                    omit_prospective_fd_indices.append(fds_copy.index(prospective_fd))
                else:
                    prospective_fd.start_chunk = selected_fd.end_chunk
                break
    for i in sorted(omit_prospective_fd_indices, reverse=True):
        del fds_copy[i]
    return fds_copy


class InitialFileSelectRail(Rail):
    # Select files given issue and files in repo
    prompt_spec = f"""Hey, somebody just opened an issue in my repo, could you help me write a pull request?

The issue is:
```{{issue}}```

The list of files in the repo is:
```{{filepaths_with_token_lengths}}```

Should we take a look at any files? If so, pick only a few files (max {{token_limit}} tokens). 
If looking at files would be a waste of time with regard to the issue, let me know."""

    output_type = InitialFileSelectResponse
    extra_params = {
        'temperature': 0,
    }

    issue: str
    file_descriptors: list[FileDescriptor]
    token_limit: int

    def get_string_params(self) -> dict[str, str]:
        return {
            'issue': self.issue,
            'filepaths_with_token_lengths': '\n'.join([
                file_descriptor.filepaths_with_token_lengths_to_str()
                for file_descriptor in self.file_descriptors
            ]),
            'token_limit': str(self.token_limit),
        }

    def get_rail_spec(cls):
        return f"""
<rail version="0.1">
<output>
{cls.output_type.rail_spec}
</output>
<prompt>
```
{{{{raw_response}}}}
```

@xml_prefix_prompt

{{output_schema}}

If looking at files would be a waste of time, please submit an empty list.

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""


class LookAtFiles(Rail):
    # Select files given issue, unseen files in repo, and notes
    prompt_spec = f"""Hey, somebody just submitted an issue, could you own it, and write a pull request?

The issue that was opened:
```{{issue}}```

We've decided to look at these files:
```{{codebase}}```

The list of files in the repo that we haven't taken a look at yet:
```{{filepaths_with_token_lengths}}```

Take some notes that will help us plan our code commits, in an effort to close the issue. 
Also, should we take a look at any other files? If so, pick only a few files (max {{token_limit}} tokens). 
If looking at files would be a waste of time with regard to the issue, let me know."""

    output_type = LookAtFilesResponse
    extra_params = {
        'temperature': 0.2,
    }

    issue: str
    selected_file_contents: list[FileDescriptor]
    prospective_file_descriptors: list[FileDescriptor]
    token_limit: int
    _filtered_prospective_file_descriptors: Optional[list[FileDescriptor]] = pydantic.PrivateAttr(None)

    def get_string_params(self) -> dict[str, str]:
        self._filtered_prospective_file_descriptors = _filter_seen_chunks(
            self.selected_file_contents, self.prospective_file_descriptors
        )

        return {
            'issue': self.issue,
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
        return _trim_chunk(self.selected_file_contents)

    def get_rail_spec(cls):
        return f"""
<rail version="0.1">
<output>
{cls.output_type.rail_spec}
</output>
<prompt>
```
{{{{raw_response}}}}
```

@xml_prefix_prompt

{{output_schema}}

If looking at more files would be a waste of time, please submit an empty list.

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""


class ContinueLookingAtFiles(Rail):
    # Continue selecting files and generating fp_notes given issue, unseen files in repo, and notes
    prompt_spec = f"""Hey, somebody just submitted an issue, could you own it, and write a pull request?

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
    extra_params = {
        'temperature': 0.2,
    }

    issue: str
    notes: str
    selected_file_contents: list[FileDescriptor]
    prospective_file_descriptors: list[FileDescriptor]
    token_limit: int
    _filtered_prospective_file_descriptors: Optional[list[FileDescriptor]] = pydantic.PrivateAttr(None)

    def get_string_params(self) -> dict[str, str]:
        self._filtered_prospective_file_descriptors = _filter_seen_chunks(
            self.selected_file_contents, self.prospective_file_descriptors
        )

        return {
            'issue': self.issue,
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
        return _trim_chunk(self.selected_file_contents)


class ProposePullRequest(Rail):
    # Generate proposed list of commit messages, given notes and issue
    prompt_spec = f"""Hey somebody just submitted an issue, could you own it, write some commits, and a pull request?

These are notes we took while looking at the repo:
```{{notes_taken_while_looking_at_files}}```

This is the issue that was opened:
```{{issue}}```

When you're done, send me the pull request title, body, and a list of commits coupled with which files we should look at to write the commit's code."""

    output_type = PullRequestDescription
    extra_params = {
        'temperature': 0.1,
    }

    notes_taken_while_looking_at_files: str
    issue: str


class NewDiff(Rail):
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
Only write a unidiff in the codebase subset we're looking at.
If the codebase subset is not relevant to the commit, send me an empty unidiff."""

    output_type = Diff
    extra_params = {
        'temperature': 0.0,
    }

    issue: str
    pull_request_description: str
    selected_file_contents: list[FileDescriptor]
    commit: str

    def get_string_params(self) -> dict[str, str]:
        return {
            'issue': self.issue,
            'pull_request_description': self.pull_request_description,
            'codebase': '\n'.join([
                file_descriptor.filenames_and_contents_to_str()
                for file_descriptor in self.selected_file_contents
            ]),
            'commit': self.commit,
        }

    def trim_params(self) -> bool:
        return _trim_chunk(self.selected_file_contents)


RailUnion = Union[tuple(Rail.__subclasses__())]  # type: ignore

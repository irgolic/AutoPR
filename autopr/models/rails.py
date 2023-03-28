import typing
from typing import ClassVar, Union, Optional, Any
from typing_extensions import TypeAlias

import pydantic

from autopr.models.rail_objects import LookAtFilesResponse, PullRequestDescription, \
    InitialFileSelectResponse, RailObject, Diff

import structlog

from autopr.utils.repo import FileDescriptor, filter_seen_chunks, trim_chunk

log = structlog.get_logger()


class Rail(pydantic.BaseModel):
    prompt_spec: ClassVar[str] = ''
    extra_params: ClassVar[dict[str, Any]] = {}
    output_type: ClassVar[typing.Type[RailObject]]

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

@complete_json_suffix_v2
</prompt>
</rail>
"""


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

If looking at files would be a waste of time, please submit an empty list.

@complete_json_suffix_v2
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
        self._filtered_prospective_file_descriptors = filter_seen_chunks(
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
        return trim_chunk(self.selected_file_contents)

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

If looking at more files would be a waste of time, please submit an empty list.

@complete_json_suffix_v2
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
        self._filtered_prospective_file_descriptors = filter_seen_chunks(
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
        return trim_chunk(self.selected_file_contents)


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
Only write a unidiff in the codebase subset we're looking at."""

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
        return trim_chunk(self.selected_file_contents)


RailUnion: TypeAlias = Union[tuple(Rail.__subclasses__())]  # type: ignore

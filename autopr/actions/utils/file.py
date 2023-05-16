import json
import os
from collections import defaultdict
from typing import Optional, Any

from git.repo import Repo

from autopr.actions.base import ContextDict
from autopr.actions.utils.commit import CommitPlan
from autopr.models.prompt_chains import PromptChain

import pydantic

from langchain.schema import BaseOutputParser

import structlog
log = structlog.get_logger()


###
# File hunk generation
###


class GeneratedFileHunk(pydantic.BaseModel):
    """
    A generated hunk of code, followed by the outcome of the generation.
    TODO explore better ways of reflecting on the output of the generation than `outcome`.
    """
    contents: str
    outcome: str


class GeneratedHunkOutputParser(BaseOutputParser):
    """
    An output parser for the generated hunk, in the format of:
        ```
        <string>
        ```
        {
            "outcome": <string>
        }
    """
    def parse(self, output: str) -> Optional[GeneratedFileHunk]:
        output_lines = output.split("\n")

        try:
            # Filter through the output until the first ``` is found
            while not output_lines[0].startswith("```"):
                output_lines.pop(0)
            output_lines.pop(0)

            # Find the last ``` line
            reversed_lines = output_lines[::-1]
            while not reversed_lines[0].startswith("```"):
                reversed_lines.pop(0)
            reversed_lines.pop(0)
            lines = reversed_lines[::-1]

            code = "\n".join(lines)

            # Retrieve the JSON
            json_lines = output_lines[len(lines) + 1:]
            try:
                outcome = json.loads("\n".join(json_lines))["outcome"]
            except json.JSONDecodeError:
                outcome = ""
        except:
            # TODO reask to fix the output
            return None
        return GeneratedFileHunk(
            contents=code,
            outcome=outcome,
        )

    def get_format_instructions(self) -> str:
        return """RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please use the following format. Make sure you return both the code enclosed in backticks and the JSON immediately after.

```
<string>
```
{
    "outcome": string  # A description of the outcome of the attempt to rewrite the file hunk according to the problem statement.
}
"""


###
# File context creation
###


class ContextCodeHunk(pydantic.BaseModel):
    """
    A hunk of code that is part of the context for code generation.
    """
    highlight_line_numbers: list[int] = pydantic.Field(default_factory=list)
    code_hunk: list[tuple[int, str]]

    def __str__(self):
        if not self.code_hunk:
            return ''
        max_line_num_width = len(str(self.code_hunk[-1][0]))
        lines = []
        for num, line_content in self.code_hunk:
            num_width = len(str(num))
            line = ' ' * (max_line_num_width - num_width) + str(num)
            if num in self.highlight_line_numbers:
                line += ' * '
            else:
                line += ' | '
            line += line_content
            lines.append(line)
        return '\n'.join(lines)


class ContextFile(pydantic.BaseModel):
    """
    A file that is part of the context for code generation.
    """
    filepath: str
    code_hunks: list[ContextCodeHunk]

    def __str__(self):
        code_hunks_s = '\n\n'.join(
            [str(code_hunk) for code_hunk in self.code_hunks]
        )
        return f">>> File: {self.filepath}\n\n" + code_hunks_s


def split_into_lines(text: str) -> list[str]:
    lines = text.splitlines()
    # If text ends with a newline, we want to keep that as a line
    if text.rstrip() != text:
        lines.append("")
    return lines


def get_lines(
    repo: Repo,
    filepath: str,
    start_line: Optional[int] = None,
    end_line: Optional[int] = None,
) -> Optional[list[tuple[int, str]]]:
    working_dir = repo.working_tree_dir
    assert working_dir is not None
    path = os.path.join(working_dir, filepath)
    if not os.path.exists(path):
        log.error(f"File {filepath} not in repo")
        return None
    if not os.path.isfile(path):
        log.error(f"{filepath} is not a file")
        return None

    with open(path, 'r') as f:
        lines = split_into_lines(f.read())
    code_hunk: list[tuple[int, str]] = []

    # Get and limit line numbers
    start_line = start_line or 1
    start_line = min(max(start_line, 1), len(lines))
    end_line = end_line or len(lines)
    end_line = min(max(end_line, 1), len(lines))
    end_line = max(start_line, end_line)

    for line_num in range(start_line, end_line + 1):
        code_hunk.append((line_num, lines[line_num - 1]))
    return code_hunk


def make_file_context(
    repo: Repo,
    commit: CommitPlan,
) -> list[ContextFile]:
    hunks_by_filepath = defaultdict(list)
    for hunk in commit.relevant_file_hunks:
        fp = hunk.filepath
        hunks_by_filepath[fp].append(hunk)

    context = []
    for fp, hunks in hunks_by_filepath.items():
        code_hunks = []
        for hunk in hunks:
            lines = get_lines(
                repo=repo,
                filepath=fp,
                start_line=hunk.start_line,
                end_line=hunk.end_line,
            )
            if lines is None:
                continue
            code_hunks.append(
                ContextCodeHunk(
                    code_hunk=lines,
                )
            )

        if code_hunks:
            context.append(
                ContextFile(
                    filepath=fp,
                    code_hunks=code_hunks,
                )
            )

    return context


def add_element_to_context_list(
    context: ContextDict,
    key: str,
    element: Any,
) -> ContextDict:
    if key not in context:
        context[key] = []
    context[key].append(element)
    return context

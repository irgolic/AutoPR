import os
import re
from typing import Union, Any, Dict, List, Optional

from git import GitCommandError
from pydantic import ValidationError

from autopr.models.rail_objects import Diff
from autopr.services.diff_service import DiffService
from guardrails import register_validator, Validator
from guardrails.validators import EventDetail
import git

import structlog
log = structlog.get_logger()


def adjust_line_indentation(line: str, indentation_offset: int) -> str:
    if indentation_offset >= 0:
        return indentation_offset * ' ' + line
    else:
        return line[-indentation_offset:]


def remove_hallucinations(lines: List[str], tree: git.Tree) -> List[str]:
    cleaned_lines: list[str] = []
    current_file_content: Optional[list[str]] = None
    current_line_number: int = 0
    search_range: int = 20
    first_line_semaphore: int = 0
    indentation_offset: int = 0
    is_new_file: bool = False

    for i, line in enumerate(lines):
        first_line_semaphore = max(0, first_line_semaphore - 1)
        if line.startswith("---") and lines[i + 1].startswith("+++") and lines[i + 2].startswith("@@"):  # hunk header
            is_new_file = False

            # Extract the filename after ---
            filepath_match = re.match(r"--- (.+)", line)
            filepath = filepath_match.group(1)

            # Get the file content
            try:
                blob = tree / filepath
                current_file_content = blob.data_stream.read().decode().splitlines()
            except KeyError:
                is_new_file = True
                current_file_content = None
                current_line_number = 0

            cleaned_lines.append(line)
        elif line.startswith("@@"):  # line count (hunk header 3/3)
            match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if match is None:
                current_line_number = 1
                cleaned_lines.append("@@ -1,0 +1,0 @@")
            else:
                current_line_number = int(match.group(1)) - 1
                cleaned_lines.append(line)
            indentation_offset = 0
            first_line_semaphore = 2
        elif line.startswith("+++"):  # filename (hunk header 2/2)
            cleaned_lines.append(line)
        elif line.startswith("-"):  # remove line
            if is_new_file:
                continue
            line_content = line[1:]
            if current_line_number >= len(current_file_content):
                continue
            file_line = current_file_content[current_line_number]
            # Put the right line into the diff
            cleaned_lines.append(f"-{file_line}")
            current_line_number += 1
            if line_content.lstrip() != file_line.lstrip():
                continue
            if (
                line_content != file_line and
                line_content.lstrip() == file_line.lstrip()
            ):
                # Fix indentation also in + lines
                real_indentation = len(file_line) - len(file_line.lstrip())
                hallucinated_indentation = len(line_content) - len(line_content.lstrip())
                indentation_offset = real_indentation - hallucinated_indentation
        elif line.startswith("+"):  # new line
            if line[1:]:
                cleaned_lines.append(f"+{adjust_line_indentation(line[1:], indentation_offset)}")
            else:
                cleaned_lines.append("+")
        elif line.lstrip() != line:  # context line
            # Line has a leading whitespace, check if it's in the actual file content
            if is_new_file or current_line_number >= len(current_file_content):
                continue
            file_line = current_file_content[current_line_number]
            if line.lstrip() == file_line.lstrip():
                # If indentation is wrong, use that
                if indentation_offset:
                    if not file_line:
                        cleaned_lines.append(" ")
                    else:
                        cleaned_lines.append(f" {adjust_line_indentation(line[1:], indentation_offset)}")
                else:  # Else, use the real line
                    cleaned_lines.append(f" {file_line}")
                    # Fix indentation also in + lines
                    real_indentation = len(file_line) - len(file_line.lstrip())
                    hallucinated_indentation = len(line[1:]) - len(line.lstrip())
                    indentation_offset = real_indentation - hallucinated_indentation
                current_line_number += 1
            elif first_line_semaphore:
                # Search for the line in the file content
                # Organize the search range from the current line number outward
                search_offset_list = list(range(-search_range, search_range + 1))
                search_offset_list.sort(key=abs)
                for offset in search_offset_list:
                    check_line_number = current_line_number + offset
                    if not 0 <= check_line_number < len(current_file_content):
                        continue
                    check_file_line = current_file_content[check_line_number]
                    if line.lstrip() == check_file_line.lstrip():
                        current_line_number = check_line_number + 1
                        # Fix @@ line
                        cleaned_lines[-1] = f"@@ -{check_line_number + 1},1 +{check_line_number + 1},1 @@"
                        cleaned_lines.append(f' {check_file_line}')
                        break
            elif file_line == "":
                # Look forward for the line, as long as you're looking through empty lines
                for check_line_number in range(current_line_number + 1, len(current_file_content)):
                    check_file_line = current_file_content[check_line_number]
                    if check_file_line == "":
                        continue
                    if line.lstrip() != check_file_line.lstrip():
                        break
                    # Add as many newlines as needed
                    newline_count = check_line_number - current_line_number
                    cleaned_lines += [" "] * newline_count
                    cleaned_lines.append(f' {check_file_line}')
                    current_line_number = check_line_number + 1
                    break
        else:
            if not line:
                cleaned_lines.append(line)
                current_line_number += 1
            else:
                log.warning("Unknown line: ", line=line)

    if cleaned_lines[-1] != "":
        cleaned_lines[-1] = ""
    return cleaned_lines


def create_unidiff_validator(repo: git.Repo, diff_service: DiffService):
    class Unidiff(Validator):
        """Validate value is a valid unidiff.
        - Name for `format` attribute: `unidiff`
        - Supported data types: `string`
        """

        def validate_with_correction(self, key, value, schema) -> Dict:
            error_event = EventDetail(key, value, schema, "", None)
            fixed_schema = self.fix(error_event)
            fixed_value = fixed_schema[key]

            try:
                self.validate(key, fixed_value, fixed_schema)
            except EventDetail:
                log.warning("Failed to fix unidiff", key=key, value=value)
                schema[key] = None

            return schema

        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
            log.debug(f"Validating unidiff...", value=value)

            try:
                model = Diff.parse_obj({'hunks': value})
                diff_service.apply_diff(model.to_str(), check=True)
            except (GitCommandError, ValidationError) as e:
                raise EventDetail(
                    key,
                    value,
                    schema,
                    e.stderr,
                    None,
                )

            return schema

        def fix(self, error: EventDetail) -> Any:
            log.debug("Fixing unidiff...", value=error.value)

            value = error.value
            try:
                model = Diff.parse_obj({'hunks': value})
            except ValidationError:
                return error.schema

            tree = repo.head.commit.tree

            # Rename any hunks that start with --- a/ or +++ b/
            # for hunk in model.hunks:
            #     if hunk.file.startswith('a/'):
            #         hunk.file = hunk.file[2:]
            #     elif hunk.file.startswith('b/'):
            #         hunk.file = hunk.file[2:]

            # If file does not exist, denote it as a new file
            for hunk in model.hunks:
                if hunk.file not in tree:
                    hunk.new_file = True

            # Filter out new lines if they are the first line in a hunk
            # remove_indices = []
            # for i, line in enumerate(lines):
            #     if line.startswith("@@"):
            #         # Find the next line that isn't a space
            #         j = i + 1
            #         while lines[j] == " ":
            #             remove_indices.append(j)
            #             j += 1
            # for i in sorted(remove_indices, reverse=True):
            #     del lines[i]

            # Recalculate the @@ line and remove hallucinated lines
            # lines = remove_hallucinations(lines, tree)

            # value = "\n".join(lines)

            error.schema[error.key] = model.dict()['hunks']
            return error.schema

    return register_validator(name="unidiff", data_type="list")(Unidiff)


def create_filepath_validator(repo: git.Repo):
    # TODO I don't think we need this validator anymore
    class FilePath(Validator):
        """Validate value is a valid file path.
        - Name for `format` attribute: `filepath`
        - Supported data types: `string`
        """
        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
            log.debug("Validating filepath...", key=key, value=value)

            # Check if the filepath exists in the repo
            tree = repo.head.commit.tree
            try:
                blob = tree / value
            except KeyError:
                raise EventDetail(
                    key,
                    value,
                    schema,
                    f"File path '{value}' does not exist in the repo.",
                    None,
                )

            if blob.type != "blob":
                raise EventDetail(
                    key,
                    value,
                    schema,
                    f"File path '{value}' is not a file.",
                    None,
                )

            return schema

        def fix(self, error: EventDetail) -> Dict:
            # Fix paths like \\dir\file.txt to /dir/file.txt
            value = error.value
            if isinstance(value, str):
                value = os.path.normpath(value)
                error.schema[error.key] = value
            return error.schema

    return register_validator(name="filepath", data_type="string")(FilePath)


@register_validator(name="no-leading-whitespace", data_type="string")
class NoLeadingWhitespace(Validator):
    """Validate value does not have leading whitespace.
    - Name for `format` attribute: `no-leading-whitespace`
    - Supported data types: `string`
    """
    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        log.debug("Validating no-leading-whitespace...", key=key, value=value)

        if value.startswith(" "):
            raise EventDetail(
                key,
                value,
                schema,
                "Value must not have leading whitespace.",
                None,
            )

        return schema

    def fix(self, error: EventDetail) -> Dict:
        value = error.value
        if not isinstance(value, str):
            value = str(value)

        # TODO overwrite `indent` if indentation is more than one space

        # Strip the value
        value = value.lstrip()

        error.schema[error.key] = value
        return error.schema

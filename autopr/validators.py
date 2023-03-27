import os
import re
from typing import Union, Any, Dict, List, Optional

from git import GitCommandError, Tree, Blob

from autopr.services.diff_service import DiffService
from guardrails import register_validator, Validator
from guardrails.validators import EventDetail
from git.repo import Repo

import structlog
log = structlog.get_logger()


def fix_unidiff_line_counts(lines: list[str]) -> list[str]:
    # TODO also fix unidiff line numbers
    corrected_lines = []

    for i, line in enumerate(lines):
        if line.startswith("@@"):
            # Extract the original x and y values
            match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if match is None:
                start_x, start_y = 0, 0
            else:
                start_x, start_y = int(match.group(1)), int(match.group(2))

            # Calculate the correct y values based on the hunk content
            x_count, y_count = 0, 0
            j = i + 1
            while j < len(lines):
                # Check if the next hunk is detected
                if (
                    j + 2 < len(lines) and
                    lines[j].startswith("---") and
                    lines[j + 1].startswith("+++") and
                    lines[j + 2].startswith("@@")
                ) or lines[j].startswith("@@"):
                    break

                if lines[j].startswith("-"):
                    x_count += 1
                elif lines[j].startswith("+"):
                    y_count += 1
                elif lines[j]:
                    x_count += 1
                    y_count += 1

                j += 1

            # Update the @@ line with the correct y values
            corrected_line = f"@@ -{start_x},{x_count} +{start_y},{y_count} @@"
            corrected_lines.append(corrected_line)
        else:
            corrected_lines.append(line)

    return corrected_lines


def adjust_line_indentation(line: str, indentation_offset: int) -> str:
    if indentation_offset >= 0:
        return indentation_offset * ' ' + line
    else:
        return line[-indentation_offset:]


def remove_hallucinations(lines: List[str], tree: Tree) -> List[str]:
    cleaned_lines: list[str] = []
    current_file_content: Optional[list[str]] = None
    current_line_number: int = 0
    search_range: int = 20
    first_line_semaphore: int = 0
    indentation_offset: int = 0

    for i, line in enumerate(lines):
        first_line_semaphore = max(0, first_line_semaphore - 1)
        if line.startswith("---") and lines[i + 1].startswith("+++") and lines[i + 2].startswith("@@"):  # hunk header

            # Extract the filename after ---
            filepath_match = re.match(r"--- (.+)", line)
            if filepath_match is None:
                log.error("Invalid diff", diff=lines)
                raise ValueError(f"Invalid diff line: {line}")
            filepath = filepath_match.group(1)

            # Get the file content
            try:
                blob = tree / filepath
                current_file_content = blob.data_stream.read().decode().splitlines()
            except KeyError:
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
            if current_file_content is None:
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
            if current_file_content is None or current_line_number >= len(current_file_content):
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


def create_unidiff_validator(repo: Repo, diff_service: DiffService):
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

        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Union[Dict, List]:
            log.debug(f"Validating unidiff...", value=value)

            try:
                diff_service.apply_diff(value, check=True)
            except GitCommandError as e:
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

            tree = repo.head.commit.tree
            value = error.value
            lines = value.splitlines()

            # Drop any `diff --git` lines
            lines = [line for line in lines if not line.startswith("diff --git")]

            # Remove whitespace in front of --- lines if it's there
            for i, line in enumerate(lines):
                stripped_line = line.lstrip()
                if stripped_line.startswith("---") and \
                        lines[i + 1].startswith("+++") and \
                        lines[i + 2].startswith("@@"):
                    lines[i] = stripped_line

            # Add space at the start of any line that's empty, except if it precedes a --- line, or is the last line
            for i, line in enumerate(lines):
                if len(lines) < i + 2:
                    break
                if line == "" and not lines[i + 1].startswith("---") and i != len(lines) - 1:
                    lines[i] = " "

            # Ensure the whole thing ends with a newline
            if not lines[-1] == "":
                lines.append("")

            # If there are any +++ @@ lines, without a preceding --- line,
            # add a `--- /dev/null` line before it
            insert_indices: list[int] = []
            for i, line in enumerate(lines):
                if line.startswith("+++ ") and lines[i + 1].startswith('@@ ') and not lines[i - 1].startswith("---"):
                    insert_indices.append(i)
            for i, index in enumerate(insert_indices):
                lines.insert(index + i, "--- /dev/null")

            # Rename any hunks that start with --- a/ or +++ b/
            for i, line in enumerate(lines):
                if len(lines) < i + 2:
                    break
                if line.startswith("--- /dev/null") and lines[i + 1].startswith("+++ b/"):
                    lines[i + 1] = lines[i + 1].replace("+++ b/", "+++ ")
                elif line.startswith("--- a/") and lines[i + 1].startswith("+++ b/"):
                    lines[i] = line.replace("--- a/", "--- ")
                    lines[i + 1] = lines[i + 1].replace("+++ b/", "+++ ")

            # Fix filenames, such that in every block of three consecutive --- +++ @@ lines,
            # the filename after +++ matches the filename after ---
            # Except the filename after --- is /dev/null
            for i, line in enumerate(lines):
                if line.startswith("---") and not line.startswith("--- /dev/null"):
                    # Extract the filename after ---
                    filename_match = re.match(r"--- (.+)", line)
                    if filename_match is None:
                        filename = "new_file"
                    else:
                        filename = filename_match.group(1)

                    # Check if the next line starts with +++ and the line after that starts with @@
                    if i + 1 < len(lines) and lines[i + 1].startswith("+++") and \
                            i + 2 < len(lines) and lines[i + 2].startswith("@@"):
                        # Update the next line's filename to match the filename after ---
                        lines[i + 1] = f"+++ {filename}"

            # If the file referenced on --- and +++ lines is not in the repo, replace it with /dev/null
            for i, line in enumerate(lines):
                if line.startswith("---") and lines[i + 1].startswith("+++") and lines[i + 2].startswith("@@"):
                    # Extract the filename after +++
                    filename_match = re.match(r"\+\+\+ (.+)", lines[i + 1])
                    if filename_match is None:
                        filename = "new_file"
                    else:
                        filename = filename_match.group(1)

                    # Check if the file is in the tree
                    if filename not in tree:
                        # See if any of the filepaths in the tree end with the filename
                        # If so, use that as the filename
                        for tree_file in tree.traverse():
                            if not isinstance(tree_file, Blob):
                                continue

                            path = tree_file.path
                            if path.endswith(filename):
                                lines[i] = f"--- {path}"
                                lines[i + 1] = f"+++ {path}"
                                break
                        else:
                            lines[i] = f"--- /dev/null"

            # If there is a lone @@ line, prefix it with the --- and +++ lines from the previous block
            current_block: list[str] = []
            insertions: list[tuple[int, list[str]]] = []
            for i, line in enumerate(lines):
                if line.startswith("---") and lines[i + 1].startswith("+++ ") and lines[i + 2].startswith("@@"):
                    current_block = [lines[i], lines[i + 1]]
                if line.startswith("@@") and not lines[i - 1].startswith("+++ "):
                    insertions.append((i, current_block))
            for i, (index, newlines) in enumerate(insertions):
                actual_index = index + i * 2
                lines.insert(actual_index, newlines[0])
                lines.insert(actual_index + 1, newlines[1])

            # If it's a new file (--- starts with /dev/null), make all the lines in the hunk start with +
            for i, line in enumerate(lines):
                if line.startswith("--- /dev/null") and lines[i + 1].startswith("+++ ") and lines[i + 2].startswith("@@"):
                    j = i + 3
                    while j < len(lines) and not (lines[j].startswith("---") and lines[j + 1].startswith("+++") and lines[j + 2].startswith("@@")):
                        if lines[j].startswith(" "):
                            lines[j] = "+" + lines[j][1:]
                        elif lines[j].startswith("-"):
                            lines[j] = "+" + lines[j][1:]
                        elif not lines[j].startswith("+"):
                            lines[j] = "+" + lines[j]
                        j += 1

            # Filter out new lines if they are the first line in a hunk
            remove_indices = []
            for i, line in enumerate(lines):
                if line.startswith("@@"):
                    # Find the next line that isn't a space
                    j = i + 1
                    while lines[j] == " ":
                        remove_indices.append(j)
                        j += 1
            for i in sorted(remove_indices, reverse=True):
                del lines[i]

            # Recalculate the @@ line and remove hallucinated lines
            lines = remove_hallucinations(lines, tree)

            # Recalculate the line counts in the unidiff
            lines = fix_unidiff_line_counts(lines)

            value = "\n".join(lines)

            error.schema[error.key] = value
            return error.schema

    return register_validator(name="unidiff", data_type="string")(Unidiff)


def create_filepath_validator(repo: Repo):
    # TODO I don't think we need this validator anymore
    class FilePath(Validator):
        """Validate value is a valid file path.
        - Name for `format` attribute: `filepath`
        - Supported data types: `string`
        """
        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Union[Dict, List]:
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

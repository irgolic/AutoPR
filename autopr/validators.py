import logging
import re
import tempfile
from typing import Union, Any, Dict, List

from git import GitCommandError

from guardrails import register_validator, Validator
from guardrails.validators import EventDetail
import git

logger = logging.getLogger(__name__)


def fix_unidiff_line_counts(lines: list[str]) -> list[str]:
    # TODO also fix unidiff line numbers
    corrected_lines = []

    for i, line in enumerate(lines):
        if line.startswith("@@"):
            # Extract the original x and y values
            match = re.match(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
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
                ):
                    break

                if lines[j].startswith("-"):
                    x_count += 1
                elif lines[j].startswith("+"):
                    y_count += 1
                elif not lines[j].startswith("\\"):
                    x_count += 1
                    y_count += 1

                j += 1

            # Update the @@ line with the correct y values
            corrected_line = f"@@ -{start_x},{x_count - 1} +{start_y},{y_count - 1} @@"
            corrected_lines.append(corrected_line)
        else:
            corrected_lines.append(line)

    return corrected_lines


def remove_hallucinated_lines(lines: list[str], tree: git.Tree) -> list[str]:
    cleaned_lines = []
    current_file_content = None
    current_line_number = 0
    search_range = 1
    first_line = 0

    for i, line in enumerate(lines):
        first_line = max(0, first_line - 1)
        if line.startswith("---") and lines[i + 1].startswith("+++") and lines[i + 2].startswith("@@"):
            # Extract the filename after ---
            filepath_match = re.match(r"--- (.+)", line)
            filepath = filepath_match.group(1)

            # Get the file content
            try:
                blob = tree / filepath
                current_file_content = blob.data_stream.read().decode().splitlines()
            except KeyError:
                # TODO remove hunk
                current_file_content = None
                current_line_number = 0

            cleaned_lines.append(line)
        elif line.startswith("@@"):
            current_line_number = int(re.match(r"@@ -(\d+),\d+ \+\d+,\d+ @@", line).group(1)) - 1
            cleaned_lines.append(line)
            first_line = 2
        elif line.startswith("+++"):
            cleaned_lines.append(line)
        elif line.startswith("-"):
            if current_file_content and current_line_number < len(current_file_content):
                if line[1:] == current_file_content[current_line_number]:
                    cleaned_lines.append(line)
                else:
                    # Put the right line into the diff
                    cleaned_lines.append(f"-{current_file_content[current_line_number]}")
                current_line_number += 1
        elif line.startswith("+"):
            cleaned_lines.append(line)
        elif line.lstrip() != line:
            # Line has a leading whitespace, check if it's in the actual file content
            if current_file_content:
                if current_line_number < len(current_file_content) and line[1:] == current_file_content[current_line_number]:
                    # Line is in the file content
                    cleaned_lines.append(line)
                    current_line_number += 1
                elif first_line:
                    # Search for the line in the file content
                    for offset in range(-search_range, search_range + 1):
                        check_line_number = current_line_number + offset
                        check_file_line = current_file_content[check_line_number]
                        if 0 <= check_line_number < len(current_file_content) and line[1:] == check_file_line:
                            current_line_number = check_line_number + 1
                            # Fix @@ line
                            cleaned_lines[-1] = re.sub(r"(\d+),\d+", f"{check_line_number + 1},1", cleaned_lines[-1])
                            cleaned_lines.append(line)
                            break
        else:
            cleaned_lines.append(line)
            current_line_number += 1

    return cleaned_lines


def create_unidiff_validator(repo: git.Repo, tree: git.Tree):
    class Unidiff(Validator):
        """Validate value is a valid unidiff.
        - Name for `format` attribute: `unidiff`
        - Supported data types: `string`
        """

        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
            logger.debug(f"Validating {value} is unidiff...")

            # try to apply the patch with git apply --check
            with tempfile.NamedTemporaryFile() as f:
                f.write(value.encode())
                f.flush()
                try:
                    repo.git.execute(["git", "apply", "--check", "--unidiff-zero", "--ignore-whitespace", f.name])
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

            # Rename any hunks that start with --- a/ or +++ b/
            for i, line in enumerate(lines):
                if len(lines) < i + 2:
                    break
                if line.startswith("--- a/") and lines[i + 1].startswith("+++ b/"):
                    lines[i] = line.replace("--- a/", "--- ")
                    lines[i + 1] = lines[i + 1].replace("+++ b/", "+++ ")

            # Add space at the start of any line that's empty, except if it precedes a --- line, or is the last line
            for i, line in enumerate(lines):
                if len(lines) < i + 2:
                    break
                if line == "" and not lines[i + 1].startswith("---") and i != len(lines) - 1:
                    lines[i] = " "

            # Ensure the whole thing ends with a newline
            if not lines[-1] == "":
                lines.append("")

            # Fix filenames, such that in every block of three consecutive --- +++ @@ lines,
            # the filename after +++ matches the filename after ---
            # Except the filename after --- is /dev/null
            for i, line in enumerate(lines):
                if line.startswith("---") and not line.startswith("--- /dev/null"):
                    # Extract the filename after ---
                    filename_match = re.match(r"--- (.+)", line)
                    filename = filename_match.group(1)

                    # Check if the next line starts with +++ and the line after that starts with @@
                    if i + 1 < len(lines) and lines[i + 1].startswith("+++") and \
                            i + 2 < len(lines) and lines[i + 2].startswith("@@"):
                        # Update the next line's filename to match the filename after ---
                        lines[i + 1] = f"+++ {filename}"

            # Remove any hallucinated lines prefixed with whitespace
            lines = remove_hallucinated_lines(lines, tree)

            # Recalculate the line counts in the unidiff
            lines = fix_unidiff_line_counts(lines)

            value = "\n".join(lines)

            try:
                self.validate(error.key, value, error.schema)
            except EventDetail:
                return super().fix(error)

            error.schema[error.key] = value
            return error.schema

    return register_validator(name="unidiff", data_type="string")(Unidiff)


def create_filepath_validator(tree: git.Tree):
    class FilePath(Validator):
        """Validate value is a valid file path.
        - Name for `format` attribute: `filepath`
        - Supported data types: `string`
        """
        def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
            # Check if the filepath exists in the repo
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

    return register_validator(name="filepath", data_type="string")(FilePath)

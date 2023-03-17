import logging
import os
import re
import tempfile
from typing import Union, Any, Dict, List

import unidiff
import unidiff.errors
from git import GitCommandError

from guardrails import register_validator, Validator
from guardrails.validators import EventDetail
import git

logger = logging.getLogger(__name__)


@register_validator(name="patch", data_type="string")
class GitPatch(Validator):
    """Validate value is a valid git patch.
    - Name for `format` attribute: `patch`
    - Supported data types: `string`
    """

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        logger.debug(f"Validating {value} is git patch...")
        repo_path = os.environ["GITHUB_WORKSPACE"]
        repo = git.Repo(repo_path)

        # randstr = os.urandom(16).hex()
        # filename = f"patch-{randstr}.diff"
        # if os.path.exists(filename):
        #     os.remove(filename)
        # with open(filename, "w") as f:

        # Create a temporary file with tempfile.NamedTemporaryFile
        # and pass the file path to git apply --check
        with tempfile.NamedTemporaryFile() as f:
            f.write(value.encode())
            f.flush()
            try:
                out_str = repo.git.execute(["git", "apply", "--check", f.name])
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
        # Try fixing by removing the "index 0000000..0000000" line from the patch
        lines = [
            line for line in
            error.value.splitlines()
            if not line.startswith("index ")
        ]
        possibly_fixed_value = "\n".join(lines)
        try:
            return self.validate(error.key, possibly_fixed_value, error.schema)
        except EventDetail:
            pass

        return super().fix(error)


def fix_unidiff_line_counts(corrupted_unidiff: str) -> str:
    lines = corrupted_unidiff.splitlines()
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
            corrected_line = f"@@ -{start_x},{x_count} +{start_y},{y_count} @@"
            corrected_lines.append(corrected_line)
        else:
            corrected_lines.append(line)

    return "\n".join(corrected_lines)


@register_validator(name="unidiff", data_type="string")
class Unidiff(Validator):
    """Validate value is a valid unidiff.
    - Name for `format` attribute: `unidiff`
    - Supported data types: `string`
    """

    def validate(self, key: str, value: Any, schema: Union[Dict, List]) -> Dict:
        logger.debug(f"Validating {value} is unidiff...")

        if not value.endswith("\n"):
            raise EventDetail(
                key,
                value,
                schema,
                "Unidiff must end with a newline",
                None,
            )

        try:
            unidiff.PatchSet(value)
        except unidiff.errors.UnidiffParseError as e:
            raise EventDetail(
                key,
                value,
                schema,
                str(e),
                None,
            )
        return schema

    def fix(self, error: EventDetail) -> Any:
        value = error.value

        # Add space at the start of any line that's empty
        lines = [
            line if line else " "
            for line in value.splitlines()
        ]

        # Fix filenames, such that in every block of three consecutive --- +++ @@ lines,
        # the filename after +++ matches the filename after ---
        for i, line in enumerate(lines):
            if line.startswith("---"):
                # Extract the filename after ---
                filename_match = re.match(r"--- (.+)", line)
                filename = filename_match.group(1)

                # Check if the next line starts with +++ and the line after that starts with @@
                if i + 1 < len(lines) and lines[i + 1].startswith("+++") and \
                        i + 2 < len(lines) and lines[i + 2].startswith("@@"):
                    # Update the next line's filename to match the filename after ---
                    lines[i + 1] = f"+++ {filename}"

        value = "\n".join(lines)

        # Recalculate the line counts in the unidiff
        value = fix_unidiff_line_counts(value)

        # Add a newline at the end of the unidiff
        if not value.endswith("\n"):
            value += "\n"

        try:
            self.validate(error.key, value, error.schema)
        except EventDetail:
            return super().fix(error)

        # TODO try to apply the patch with git apply --check
        # and if it fails, reask

        error.schema[error.key] = value
        return error.schema

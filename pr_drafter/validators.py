import logging
import os
import tempfile
from typing import Union, Any, Dict, List

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

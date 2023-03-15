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

        # Create a temporary file with tempfile.NamedTemporaryFile
        # and pass the file path to git apply --check
        with tempfile.NamedTemporaryFile() as f:
            f.write(value.encode())
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

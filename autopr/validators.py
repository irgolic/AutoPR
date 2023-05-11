import os
import re
from typing import Union, Any, Dict, List, Optional

from git import GitCommandError, Tree, Blob

from autopr.services.diff_service import DiffService
from guardrails import register_validator, Validator
from guardrails.validators import EventDetail, Filter
from git.repo import Repo

import structlog
log = structlog.get_logger()


@register_validator(name="filepath", data_type="string")
class FilePath(Validator):
    """Validate value is a valid file path.
    - Name for `format` attribute: `filepath`
    - Supported data types: `string`
    """
    def validate(self, key: str, value: Any, schema: Dict) -> Union[Dict, List]:
        log.debug("Validating filepath...", key=key, value=value)

        # Check if filepath is a string
        if not isinstance(value, str):
            raise EventDetail(
                key,
                value,
                schema,
                f"File path '{value}' is not a string.",
                None,
            )

        # Is it normalized?
        if value != os.path.normpath(value):
            raise EventDetail(
                key,
                value,
                schema,
                f"File path '{value}' is not normalized.",
                None,
            )

        # Check that it's not a directory
        # The directory does not need to exist, so we can't use os.path.isdir
        if value.endswith(os.sep):
            raise EventDetail(
                key,
                value,
                schema,
                f"File path '{value}' is a directory.",
                None,
            )

        return schema

    def fix(self, error: EventDetail) -> Dict:
        value = error.value

        # Check if filepath is a string
        if not isinstance(value, str):
            error.schema[error.key] = Filter()
            return error.schema

        # Fix paths like \\dir\file.txt to /dir/file.txt
        value = os.path.normpath(value)
        error.schema[error.key] = value

        # Check that it's not a directory
        try:
            self.validate(error.key, value, error.schema)
        except EventDetail:
            error.schema[error.key] = Filter()
            return error.schema

        return error.schema

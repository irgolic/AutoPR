import typing
from typing import ClassVar, Any
import pydantic

from autopr.models.rail_objects import RailObject

import structlog

log = structlog.get_logger()


class PromptRail(pydantic.BaseModel):
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

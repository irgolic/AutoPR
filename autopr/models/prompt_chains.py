from typing import ClassVar, Any, Type, Optional
import pydantic
from langchain.schema import BaseOutputParser

from autopr.models.rail_objects import RailObject

import structlog

log = structlog.get_logger()


class PromptChain(pydantic.BaseModel):
    prompt_template: ClassVar[str] = ''
    extra_params: ClassVar[dict[str, Any]] = {}
    output_parser: ClassVar[Optional[Type[BaseOutputParser]]] = None

    def get_string_params(self) -> dict[str, str]:
        prompt_params = {}
        for key, value in self:
            if isinstance(value, list):
                prompt_params[key] = '\n\n'.join(
                    [str(item) for item in value]
                )
            else:
                prompt_params[key] = str(value)
        return prompt_params

    def trim_params(self) -> bool:
        """
        Override this method to trim the parameters of the prompt.
        This is called when the prompt is too long.
        """

        log.warning("Naively trimming params", rail=self)
        prompt_params = dict(self)
        # If there are any lists, remove the last element of the first one you find
        for key, value in prompt_params.items():
            if isinstance(value, list) and len(value) > 0:
                setattr(self, key, value[:-1])
                return True
        return False

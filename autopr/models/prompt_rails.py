import typing
from typing import ClassVar, Any
import pydantic

from autopr.models.prompt_base import PromptBase
from autopr.models.rail_objects import RailObject

import structlog

log = structlog.get_logger()


class PromptRail(PromptBase):
    """
    A prompt rail is a pydantic model used to specify a prompt for a guardrails LLM call.
    See RailObject, RailService, and [Guardrails docs](https://docs.guardrails.io/) for more information.

    To define your own prompt rail:
    - declare your output type by subclassing RailObject, and referencing it in the `output_type` class variable
    - write a prompt in the `prompt_template` class variable, referencing parameters as {param}
    - define your parameters as pydantic instance attributes
    """

    #: Whether to invoke the guardrails LLM call on the output of an ordinary LLM call, or just by itself.
    two_step: ClassVar[bool] = True

    #: The RailObject type to parse the LLM response into.
    output_type: ClassVar[typing.Type[RailObject]]

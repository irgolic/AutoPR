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
    - write a prompt template in the `prompt_spec` class variable, referencing parameters as {param}
    - define your parameters as pydantic instance attributes

    Instance attributes declared in the PromptRail are automatically filled into the
    `prompt_spec` template string, wherever they are referenced as {param}.
    """

    #: Whether to invoke the guardrails LLM call on the output of an ordinary LLM call, or just by itself.
    two_step: ClassVar[bool] = True

    #: The prompt template to use for the guardrails LLM call (reference string parameters as {param}).
    prompt_spec: ClassVar[str] = ''

    #: Extra parameters to pass to the guardrails LLM call.
    extra_params: ClassVar[dict[str, Any]] = {}

    #: The RailObject type to parse the LLM response into.
    output_type: ClassVar[typing.Type[RailObject]]

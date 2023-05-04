from typing import ClassVar, Any, Type, Optional

from autopr.models.prompt_base import PromptBase
from langchain.schema import BaseOutputParser

import structlog

log = structlog.get_logger()


class PromptChain(PromptBase):
    """
    A prompt chain is a pydantic model used to specify a prompt for a langchain call.
    See ChainService and [Langchain docs](https://docs.langchain.ai/) for more information.

    To define your own prompt chain:
    - write a prompt template in the `prompt_template` class variable, referencing parameters as {param}
    - define your parameters as pydantic instance attributes
    - optionally define an output parser as the `output_parser` class variable

    Instance attributes declared in the PromptChain are automatically filled into the
    `prompt_template` template string, wherever they are referenced as {param}.
    """

    #: The prompt template to use for the langchain call (reference string parameters as {param}).
    prompt_template: ClassVar[str] = ''

    #: Extra parameters to pass to the langchain call.
    extra_params: ClassVar[dict[str, Any]] = {}

    #: The output parser to run the response through.
    output_parser: ClassVar[Optional[Type[BaseOutputParser]]] = None

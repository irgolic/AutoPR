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


    """

    #: The output parser to run the response through.
    output_parser: ClassVar[Optional[BaseOutputParser]] = None

    def get_string_params(self) -> dict[str, str]:
        """
        Get the parameters of the prompt as a dictionary of strings.
        Add the format instructions if an output parser is specified.
        Override this method to specify your own parameters.
        """
        prompt_params = super().get_string_params()
        if self.output_parser is not None:
            prompt_params['format_instructions'] = self.output_parser.get_format_instructions()
        return prompt_params

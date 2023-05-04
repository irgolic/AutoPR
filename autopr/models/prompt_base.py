from typing import ClassVar

import pydantic
import structlog

log = structlog.get_logger()


class PromptBase(pydantic.BaseModel):
    """
    Base class for all prompt specifications.

    Prompt parameters should be specified as pydantic instance attributes.
    They will be automatically filled into the `prompt_template` string,
    wherever they are referenced as {param}.
    """

    #: The prompt template to use for the LLM call (reference string parameters as {param}).
    prompt_template: ClassVar[str] = ''

    # TODO implement extra_params in rail_service and chain_service
    #: Extra parameters to pass to the guardrails LLM call.
    # extra_params: ClassVar[dict[str, Any]] = {}

    def get_prompt_message(self) -> str:
        """
        Get the prompt message that is sent the LLM call.
        """
        spec = self.prompt_template
        prompt_params = self.get_string_params()
        return spec.format(**prompt_params)

    def get_string_params(self) -> dict[str, str]:
        """
        Get the parameters of the prompt as a dictionary of strings.
        Override this method to specify your own parameters.
        """
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

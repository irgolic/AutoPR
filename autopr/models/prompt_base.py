import pydantic
import structlog

log = structlog.get_logger()


class PromptBase(pydantic.BaseModel):
    """
    Base class for all prompt specifications.
    Assumes prompt parameters are specified as pydantic instance attributes.
    """

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

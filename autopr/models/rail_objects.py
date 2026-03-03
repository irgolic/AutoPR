import json
from typing import List, ClassVar, Optional, Union
from typing_extensions import TypeAlias

import pydantic

from autopr.models.artifacts import DiffStr


class RailObject(pydantic.BaseModel):
    """
    A RailObject is a pydantic model that represents the output of a guardrails call.
    See PromptRail and RailService, and [Guardrails docs](https://docs.guardrails.io/) for more information.

    To define your own RailObject:
    - write an XML string compatible with the guardrails XML spec in the `output_spec` class variable
    - define your parameters as pydantic instance attributes
    """

    output_spec: ClassVar[str]

    @classmethod
    def get_rail_spec(cls):
        """
        Get the XML spec template used to define the guardrails output.
        Should include a `{{raw_document}}` in the prompt section,
        which will be replaced by the input prompt/two-step LLM output.
        """
        return f"""
<rail version="0.1">
<output>
{cls.output_spec}
</output>
<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

@json_suffix_prompt_examples
</instructions>
<prompt>
Given the following document surrounded by `+++++`, answer the following questions. 
If the answer doesn't exist in the document, enter `null`.

+++++
{{{{raw_document}}}}
+++++

Extract information from this document and return a JSON that follows the correct schema.

@xml_prefix_prompt

{{output_schema}}
</prompt>
</rail>
"""

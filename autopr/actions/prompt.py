import asyncio
import copy
import itertools
import math
from typing import Any, Optional, Literal

import openai
import openai.error
import tenacity
from pydantic import BaseModel
from tenacity import wait_exponential_jitter, retry_if_exception_type

from autopr.actions.base import Action

from autopr.actions.utils.prompt_context import (
    PromptContext,
    PromptContextEntry,
    get_string_token_length,
    trim_context,
    invoke_openai,
)


class Inputs(BaseModel):
    # what model to use to generate the variable
    model: str = "gpt-3.5-turbo-16k"

    # the context headings that are used to generate the variable
    prompt_context: Optional[PromptContext] = None

    # the instructions to use to generate the variable
    instructions: str = ""

    # the prompt to use to generate the variable
    prompt: str = ""

    # max tokens to use for the prompt
    max_prompt_tokens: int = 8000

    # max tokens to use for the response
    max_response_tokens: int = 2000

    # the strategy to use to reduce prompt context length to fit within `max_prompt_tokens`
    strategy: Literal["middle out"] = "middle out"

    # the temperature to use for the response
    temperature: float = 0.6


class Outputs(BaseModel):
    result: Any


class PromptString(Action[Inputs, Outputs]):
    """
    Prompt to generate a string.
    """

    id = "prompt"

    def build_prompt_and_instructions(self, inputs: Inputs) -> tuple[str, str]:
        # Build prompt
        prompt_elements = []
        if inputs.prompt_context:
            # TODO subtract length of rest of prompt
            prompt_elements.append(
                str(
                    trim_context(
                        inputs.prompt_context,
                        inputs.max_prompt_tokens,
                        inputs.strategy,
                        inputs.model,
                    )
                )
            )
        if inputs.prompt:
            prompt_elements.append(inputs.prompt)
        prompt = "\n\n".join(prompt_elements)

        # Build instructions
        instructions = "You are a helpful assistant."
        if inputs.instructions:
            instructions += f"\n\n{inputs.instructions}"

        return prompt, instructions

    async def run(self, inputs: Inputs) -> Outputs:
        prompt, instructions = self.build_prompt_and_instructions(inputs)

        # Check cache
        key = (prompt, instructions)
        value = self.cache_service.retrieve(key)
        if value is not None:
            await self.publish_service.publish_update("Retrieved from cache.")
            return Outputs(
                result=value,
            )

        await self.publish_service.publish_code_block(
            heading="Instructions",
            code=instructions,
        )
        await self.publish_service.publish_code_block(
            heading="Prompt",
            code=prompt,
        )

        output = await invoke_openai(
            prompt, instructions, inputs.model, inputs.temperature, inputs.max_response_tokens
        )

        # Cache result
        self.cache_service.store(key, output)

        return Outputs(
            result=output,
        )


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    inputs = Inputs(
        prompt="What should I make a fruit salad with?",
        instructions="No chattering, be as concise as possible.",
        prompt_context=PromptContext(
            __root__=[
                PromptContextEntry(
                    heading="What I have in my kitchen",
                    value="Apples, bananas, oranges, potatoes, and onions.",
                )
            ]
        ),
    )
    asyncio.run(run_action_manually(action=PromptString, inputs=inputs))

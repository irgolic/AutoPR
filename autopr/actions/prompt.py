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

from autopr.actions.utils.prompt_context import PromptContext, PromptContextEntry, get_string_token_length


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

    def filter_nones(self, d):
        if isinstance(d, dict):
            return {k: self.filter_nones(v) for k, v in d.items() if v is not None}
        elif isinstance(d, list):
            return [self.filter_nones(v) for v in d if v is not None]
        return d

    @staticmethod
    def trim_context(prompt_context: PromptContext, inputs: Inputs) -> PromptContext:
        max_token_length = inputs.max_prompt_tokens
        strategy = inputs.strategy
        model = inputs.model

        total_priority = sum(entry.priority for entry in prompt_context.__root__)

        # Count tokens in context entries
        token_length = prompt_context.get_token_length(model)
        # If context is short enough, return it
        if token_length <= max_token_length:
            return prompt_context

        if strategy == "middle out":
            trimmed_text = "\n\n\n... (trimmed) ...\n\n\n"
            trimmed_text_char_length = len(trimmed_text)

            # Create a copy of context entries
            context_entries_copy = copy.deepcopy(prompt_context.__root__)
            correct_order_context = PromptContext(
                __root__=context_entries_copy,
            )

            # Sort context_entries by priority
            sorted_entries = sorted(context_entries_copy, key=lambda x: x.priority)
            # Group entries by priority
            grouped_entries = itertools.groupby(sorted_entries, key=lambda x: x.priority)
            # Calculate total length of context entries
            total_token_length = correct_order_context.get_token_length(model)
            total_char_length = len(prompt_context.as_string())
            # Estimate characters needed to trim based on token and char length, rounded up

            def get_chars_left_to_trim():
                tokens_left_to_trim = correct_order_context.get_token_length(model) - max_token_length
                chars_per_token = math.ceil(total_char_length / total_token_length)
                return tokens_left_to_trim * chars_per_token

            chars_to_trim = get_chars_left_to_trim()

            # From each priority group, trim their middle in equal amounts
            # Try to trim the necessary amount of characters from the lowest priority group first
            # If you would trim the whole content of an entry, drop it from the context instead
            for _, entries in grouped_entries:
                if chars_to_trim <= 0:
                    break
                entries = list(entries)
                if len(PromptContext(__root__=entries).as_string()) <= chars_to_trim:
                    correct_order_context.__root__ = [entry for entry in correct_order_context.__root__
                                                      if entry not in entries]
                    chars_to_trim = get_chars_left_to_trim()
                    continue
                # iteratively halve the amount of characters to trim until it fits
                while chars_to_trim > 0:
                    for entry in entries[:]:
                        if chars_to_trim <= 0:
                            break
                        entry_char_length = len(PromptContext(__root__=[entry]).as_string())
                        truncate_char_amount = min(entry_char_length // 2 + trimmed_text_char_length,
                                                   chars_to_trim + trimmed_text_char_length,
                                                   entry_char_length)
                        if truncate_char_amount >= entry_char_length - trimmed_text_char_length:
                            # Drop the entry
                            entries.remove(entry)
                            correct_order_context.__root__ = [entry for entry in correct_order_context.__root__
                                                              if entry != entry]
                            chars_to_trim = get_chars_left_to_trim()
                            continue

                        # Keep the start and end, drop the middle
                        entry_value_char_length = len(entry.value)
                        start = entry.value[:entry_value_char_length // 2 - truncate_char_amount // 2]
                        end = entry.value[entry_value_char_length // 2 + truncate_char_amount // 2:]
                        entry.value = start + "\n\n\n... (trimmed) ...\n\n\n" + end

                        chars_to_trim = get_chars_left_to_trim()

            return correct_order_context
        raise ValueError(f"Invalid strategy: {strategy}")

    def build_prompt_and_instructions(self, inputs: Inputs) -> tuple[str, str]:
        # Build prompt
        prompt_elements = []
        if inputs.prompt_context:
            # TODO subtract length of rest of prompt
            prompt_elements.append(str(self.trim_context(inputs.prompt_context, inputs)))
        if inputs.prompt:
            prompt_elements.append(inputs.prompt)
        prompt = "\n\n".join(prompt_elements)

        # Build instructions
        instructions = "You are a helpful assistant."
        if inputs.instructions:
            instructions += f"\n\n{inputs.instructions}"

        # Build guard
        return prompt, instructions

    @tenacity.retry(
        wait=wait_exponential_jitter(
            initial=1,
            max=60,
            jitter=10,
        ),
        retry=retry_if_exception_type((
            openai.error.APIError,
            openai.error.TryAgain,
            openai.error.Timeout,
            openai.error.APIConnectionError,
            openai.error.RateLimitError,
            openai.error.ServiceUnavailableError,
            openai.error.SignatureVerificationError
        )),
        stop=tenacity.stop_after_attempt(6),
    )
    async def invoke_openai(self, inputs: Inputs, prompt: str, instructions: str) -> str:
        self.log.info("Invoking OpenAI API...")
        result = await openai.ChatCompletion.acreate(
            messages=[
                {
                    "role": "system",
                    "content": instructions,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=inputs.model,
            temperature=inputs.temperature,
            max_tokens=inputs.max_response_tokens,
        )
        self.log.info("OpenAI API invoked.")
        return result['choices'][0]['message']['content']  # type: ignore[reportGeneralTypeIssues]

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

        output = await self.invoke_openai(inputs, prompt, instructions)

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
            __root__=[PromptContextEntry(
                heading="What I have in my kitchen",
                value="Apples, bananas, oranges, potatoes, and onions."
            )]
        ),
    )
    asyncio.run(
        run_action_manually(
            action=PromptString,
            inputs=inputs
        )
    )

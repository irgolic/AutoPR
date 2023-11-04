import asyncio
from typing import Optional, Literal, Union

import openai
import openai.error
from pydantic import BaseModel, Field

from autopr.actions.base import Action

from autopr.actions.utils.prompt_context import PromptContext, trim_context, invoke_openai


class Inputs(BaseModel):
    # the possible choices
    choices: list[str]

    # whether to allow multiple choices
    allow_multiple: bool = False

    # what model to use to generate the variable
    model: str = "gpt-3.5-turbo-16k"

    # the context headings that are used to generate the variable
    prompt_context: Optional[PromptContext] = None

    # additional instructions to use to generate the variable
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
    temperature: float = 0.0


class Outputs(BaseModel):
    choice: Union[str, list[str]]


class Choice(Action[Inputs, Outputs]):
    """
    Prompt to generate a string.
    """

    id = "choice"

    def build_prompt_and_instructions(self, inputs: Inputs) -> tuple[str, str]:
        choices_bullet_points = "\n".join(f"- {choice}" for choice in inputs.choices)

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
        if inputs.allow_multiple:
            prompt += f"""
            
Respond ONLY with bullet points of choices from the following list:
{choices_bullet_points}"""
        else:
            prompt += f"""

Respond ONLY with a single choice from the following list:
{choices_bullet_points}"""

        # Build instructions
        if inputs.allow_multiple:
            instructions = f"""
You are a helpful assistant making a choice. You are ONLY allowed to respond with a bullet pointed list, where each bullet point is one of the following strings:
{choices_bullet_points}"""
        else:
            instructions = f"""
You are a helpful assistant making a choice. You are ONLY allowed to respond with one of the following strings: 
{choices_bullet_points}"""
        if inputs.instructions:
            instructions += f"\n\n{inputs.instructions}"

        return prompt, instructions

    async def invoke_choice(
        self, inputs: Inputs, prompt: str, instructions: str
    ) -> Union[list[str], str]:
        choice = await invoke_openai(
            prompt, instructions, inputs.model, inputs.temperature, inputs.max_response_tokens
        )

        await self.publish_service.publish_code_block(
            heading="Generated Output",
            code=choice,
        )

        if inputs.allow_multiple:
            choices = [
                c.strip().removeprefix("-").removeprefix("*").removeprefix("•").lstrip()
                for c in choice.split("\n")
            ]
            valid_choices = []
            for c in choices:
                if c in inputs.choices:
                    valid_choices.append(c)
                else:
                    await self.publish_service.publish_update(f"Invalid choice: {choice}")
            result = valid_choices
        else:
            if choice not in inputs.choices:
                await self.publish_service.publish_update(f"Invalid choice: {choice}")
                raise RuntimeError(f"Invalid choice: {choice}")
            result = choice

        return result

    async def run(self, inputs: Inputs) -> Outputs:
        prompt, instructions = self.build_prompt_and_instructions(inputs)

        # Check cache
        key = (prompt, instructions)
        value = self.cache_service.retrieve(key)
        if value is not None:
            await self.publish_service.publish_update("Retrieved from cache.")
            return Outputs(
                choice=value,
            )

        await self.publish_service.publish_code_block(
            heading="Prompt",
            code=prompt,
        )
        await self.publish_service.publish_code_block(
            heading="Instructions",
            code=instructions,
        )

        output = await self.invoke_choice(inputs, prompt, instructions)

        # Cache result
        self.cache_service.store(key, output)

        return Outputs(
            choice=output,
        )


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    inputs = Inputs(
        choices=[
            "apples",
            "bananas",
            "oranges",
            "potatoes",
            "onions",
        ],
        prompt="What should I make a fruit salad with?",
    )
    asyncio.run(run_action_manually(action=Choice, inputs=inputs))

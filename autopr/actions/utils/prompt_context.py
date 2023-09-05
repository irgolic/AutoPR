import copy
import itertools
import math
from typing import Union, ForwardRef

import openai.error
import pydantic
import tenacity
import tiktoken
from jinja2 import Template
from tenacity import wait_exponential_jitter, retry_if_exception_type

from autopr.models.config.transform import TransformsInto, ImplementsTransformsInContext, RealType, TransformsFrom
from autopr.models.config.value_declarations import VarDeclaration, TemplateDeclaration, LambdaDeclaration, \
    ConstDeclaration
from autopr.models.executable import TemplateString, ContextDict, ContextVarPath


class PromptContextEntry(pydantic.BaseModel):
    """
    A single entry in the context heading dic
    """

    value: str
    heading: str
    priority: int = 1


class PromptContext(pydantic.BaseModel, TransformsFrom):
    """
    A dictionary mapping heading strings to context variable values.
    Overrides `__str__` to format the context in a prompt-friendly way.
    """

    @classmethod
    def _get_config_type(cls):
        return PromptContextInConfig

    __root__: list[PromptContextEntry]

    def get_token_length(self, model: str) -> int:
        return get_string_token_length(self.as_string(), model)

    def _resolve_template_string(self, template_string: TemplateString, context: ContextDict):
        return Template(template_string).render(context)

    def as_string(
        self,
        enclosure_mark: str = "```",
    ):
        """
        Format the context as a string.

        Parameters
        ----------

        variable_headings
            A dictionary mapping context keys to headings.
            If not provided, the keys will be used as headings.
        enclosure_mark
            The string to use to enclose each variable.
        """
        if len(self.__root__) == 0:
            return ""
        context_strings = []
        for heading_entry in self.__root__:
            value = heading_entry.value
            heading = heading_entry.heading
            # Format the value as a string
            if isinstance(value, list):
                valstr = "\n".join(str(item) for item in value)
            else:
                valstr = str(value)

            # Add the variable to the context string
            context_strings.append(f"""{heading}:
{enclosure_mark}
{valstr}
{enclosure_mark}""")

        return '\n\n'.join(context_strings)

    def __str__(self):
        return self.as_string()


def get_string_token_length(string: str, model: str):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(string))

###
# Config representation
###


class PromptContextInConfigBase(pydantic.BaseModel):
    """
    A base class for prompt context in config.
    """

    heading: TemplateString
    priority: int = 1


class PromptContextInConfigVar(PromptContextInConfigBase, VarDeclaration):
    """
    A variable declaration for prompt context in config.
    """


class PromptContextInConfigTemplate(PromptContextInConfigBase, TemplateDeclaration):
    """
    A template string for prompt context in config.
    """


class PromptContextInConfigLambda(PromptContextInConfigBase, LambdaDeclaration):
    """
    A lambda declaration for prompt context in config.
    """


class PromptContextInConfigConst(PromptContextInConfigBase, ConstDeclaration):
    """
    A constant declaration for prompt context in config.
    """


class PromptContextInConfig(pydantic.BaseModel, TransformsInto[PromptContext]):
    __root__: list[Union[
        PromptContextInConfigVar,
        PromptContextInConfigTemplate,
        PromptContextInConfigLambda,
        PromptContextInConfigConst,
    ]]

    @classmethod
    def transform_from_config(
        cls,
        config_var: "PromptContextInConfig",
        context: ContextDict
    ) -> PromptContext:
        return PromptContext(__root__=[
            PromptContextEntry(
                value=entry.render(context),
                heading=context.render_string(entry.heading),
                priority=entry.priority,
            ) for entry in config_var.__root__
        ])


def trim_context(prompt_context: PromptContext, max_token_length: int, strategy: str, model: str) -> PromptContext:
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
async def invoke_openai(prompt: str, instructions: str, model: str, temperature: float, max_response_tokens: int) -> str:
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
        model=model,
        temperature=temperature,
        max_tokens=max_response_tokens,
    )
    return result['choices'][0]['message']['content']  # type: ignore[reportGeneralTypeIssues]

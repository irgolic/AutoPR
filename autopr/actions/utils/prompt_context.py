import copy
from typing import Union, ForwardRef

import pydantic
import tiktoken
from jinja2 import Template

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

import json
from typing import Union, Literal, ForwardRef, Protocol, Any, Collection, Optional, ClassVar, TypeVar, Type, \
    runtime_checkable, Generic
import jinja2

import pydantic
from jinja2 import Template

# python expression
LambdaString = str

# names of context variables like `pull_request`
ContextVarName = str

# supports paths like `pull_request.title`
ContextVarPath = str

# supports jinja2 templates like `{{ pull_request.title }}`
TemplateString = str

# supports jinja2 templates in nested dicts/lists
TemplateObject = Union[TemplateString, dict[str, Any], list[Any]]
# TODO migrate to pydantic 2.0, and use a nested self-referential Union like this:
# TemplateObject = Union[TemplateString, dict[str, "TemplateObject"], list["TemplateObject"]]


class ContextDict(dict[ContextVarName, Any]):
    def get_path(self, path: ContextVarPath) -> Any:
        """
        Get a value from the context by path (e.g., `pull_request.title`).
        """
        # TODO use jsonpath_ng instead
        path_parts = path.split(".")
        value = self
        try:
            for part in path_parts:
                if isinstance(value, pydantic.BaseModel):
                    value = value.dict()
                value = value[part]
        except KeyError:
            raise RuntimeError(f"Path {path} not found in context. "
                               f"TODO catch at static-analysis time.")
        return value

    def _unpack_template(self, value: str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    def render_string(self, template: TemplateString):
        result = jinja2.Template(template).render(**self)
        return self._unpack_template(result)

    def render_nested_template(self, template: Any):
        if isinstance(template, str):
            return self.render_string(template)
        if isinstance(template, dict):
            return {key: self.render_nested_template(value)
                    for key, value in template.items()}
        if isinstance(template, list):
            return [self.render_nested_template(item) for item in template]
        return template  


control_words = [
    "quit",
    "return",
    "continue",
]
ControlWords = Literal[tuple(control_words)]  # pyright: ignore


class ExecutableId(str):
    reserved_keywords = [
        "context",
        "*",
    ] + control_words

    def __new__(cls, value):
        if value in cls.reserved_keywords:
            raise ValueError(f"{value} is a reserved keyword")
        return str.__new__(cls, value)


# TODO we should consolidate these forward refs with their definitions in `config.py`
#  workflow_service uses this, which is why it's here instead
ExecutableForwardRef = Union[
    ExecutableId,
    # ControlWords,
    ForwardRef("ActionConfigs"),  # pyright: ignore[reportGeneralTypeIssues]
    ForwardRef("WorkflowInvocation"),  # pyright: ignore[reportGeneralTypeIssues]
    ForwardRef("IterableWorkflowInvocation"),  # pyright: ignore[reportGeneralTypeIssues]
    # ForwardRef("Choice"),  # pyright: ignore[reportGeneralTypeIssues]
    ForwardRef("ContextActions"),  # pyright: ignore[reportGeneralTypeIssues]
]
StrictExecutableForwardRef = Union[
    ForwardRef("StrictExecutableId"),  # pyright: ignore[reportGeneralTypeIssues]
    # ControlWords,
    ForwardRef("ActionConfigs"),  # pyright: ignore[reportGeneralTypeIssues]
    ForwardRef("WorkflowInvocationConfigs"),  # pyright: ignore[reportGeneralTypeIssues]
    # ForwardRef("Choice"),  # pyright: ignore[reportGeneralTypeIssues]
    ForwardRef("ContextActions"),  # pyright: ignore[reportGeneralTypeIssues]
]
Executable = Union[ExecutableForwardRef, list[ExecutableForwardRef]]
# Executable = ExecutableForwardRef
StrictExecutable = Union[StrictExecutableForwardRef, list[StrictExecutableForwardRef]]
# StrictExecutable = StrictExecutableForwardRef

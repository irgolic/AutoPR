import datetime
import json
import os
import random
import re
import sys
import time
import typing
from typing import Any, Union

import yaml
from pydantic import Field

from autopr.models.config.common import StrictModel
from autopr.models.executable import ContextDict, TemplateObject, ContextVarPath, LambdaString


EVAL_CONTEXT = {
    "os": os,
    "sys": sys,
    "random": random,
    "datetime": datetime,
    "time": time,
    "re": re,
    "json": json,
    "yaml": yaml,
}


###
### Variables
###


class Variable(StrictModel):
    def render(self, context: ContextDict):
        raise NotImplementedError


class TemplateDeclaration(Variable):
    """
    A template declaration is a string that can be rendered within a context.
    """

    template: TemplateObject

    def render(self, context: ContextDict) -> Any:
        return context.render_nested_template(self.template)


class VarDeclaration(Variable):
    """
    A variable declaration is a string that references a variable (or path to nested variable) in the context.
    """

    var: ContextVarPath

    def render(self, context: ContextDict) -> Any:
        return context.get_path(self.var)


class ConstDeclaration(Variable):
    """
    A constant declaration is a string that is interpreted as a constant value.
    """

    const: Any

    def render(self, context: ContextDict):
        return self.const


class LambdaDeclaration(Variable):
    """
    A lambda declaration is a python expression that can be evaluated within a context.
    """

    lambda_: LambdaString = Field(alias="lambda")

    def render(self, context: ContextDict):
        return eval(self.lambda_, context | EVAL_CONTEXT)


class Param(StrictModel):
    name: str
    default: Union[
        TemplateObject, TemplateDeclaration, VarDeclaration, ConstDeclaration, LambdaDeclaration
    ]


class ParamDeclaration(Variable):
    """
    A parameter declaration is a string that references a parameter passed in trigger invocation.
    """

    param: Param

    def render(self, context: ContextDict) -> Any:
        if "__params__" not in context or self.param.name not in context["__params__"]:
            if any(isinstance(self.param.default, t) for t in typing.get_args(ValueDeclaration)):
                return self.param.default.render(context)  # type: ignore[reportGeneralTypeIssues]
            else:
                return context.render_nested_template(self.param.default)
        else:
            return context["__params__"][self.param.name]


ValueDeclaration = Union[
    TemplateDeclaration, VarDeclaration, ConstDeclaration, LambdaDeclaration, ParamDeclaration
]

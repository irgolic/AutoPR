import datetime
import json
import os
import random
import re
import sys
import time
import typing
from typing import Any, Union, Optional, Literal

import pydantic
from pydantic import Field
import yaml

from autopr.actions.base import get_actions_dict
from autopr.models.config.common import StrictModel, ExtraModel
from autopr.models.config.transform import TransformsFrom
from autopr.models.config.value_declarations import ValueDeclaration, EVAL_CONTEXT

from autopr.models.executable import LambdaString, ContextVarPath, ExecutableId, Executable, \
    TemplateObject, ContextVarName, ContextDict, StrictExecutable, TemplateString


# Forbid extra (incorrect) fields in models for json schema validation


###
### Context
###


# Context mixin for actions and other objects with scope (e.g. workflows)

class ContextModel(StrictModel):
    #: Which context variables to global-style include in the scope.
    # TODO implement this so that we can pass variables through without explicitly
    #  passing them from/to every workflow and action
    # global_context: dict[ContextVarName, ContextVarName] = Field(default_factory=dict)
    pass


### Context actions


class ContextAction:
    def get_executable(self, context: ContextDict) -> Optional[Executable]:
        """
        Execute the action on the context.
        """
        raise NotImplementedError


class SetVars(StrictModel, ContextAction):
    #: Set/override context values upon execution
    set_vars: dict[ContextVarName, ValueDeclaration]

    def get_executable(self, context: ContextDict) -> None:
        for key, value in self.set_vars.items():
            context[key] = value.render(context)
        return None


class Conditional(StrictModel):
    then: Executable
    else_: Optional[Executable] = Field(default=None, alias="else")

    def executable_by_condition(self, condition_result: bool) -> Optional[Executable]:
        if condition_result:
            return self.then
        elif self.else_ is not None:
            return self.else_
        return None


class IfLambda(Conditional, ContextAction):
    #: Execute a python lambda to determine whether to run the next action
    if_lambda: LambdaString = Field(
        description="A python lambda expression that returns a boolean. "
    )

    def get_executable(self, context: ContextDict) -> Optional[Executable]:
        result = eval(self.if_lambda, context | EVAL_CONTEXT)
        return self.executable_by_condition(result)


class IfExistsContext(Conditional, ContextAction):
    #: Conditional execution based on whether a context value exists
    if_in_context: Union[ContextVarName, list[ContextVarName]]

    def get_executable(self, context: ContextDict) -> Optional[Executable]:
        req = self.if_in_context if isinstance(self.if_in_context, list) else [self.if_in_context]
        result = all(path in context for path in req)
        return self.executable_by_condition(result)


class IfContextNotExists(Conditional, ContextAction):
    #: Conditional execution based on whether a context value does not exist
    if_not_in_context: Union[ContextVarName, list[ContextVarName]]

    def get_executable(self, context: ContextDict) -> Optional[Executable]:
        req = self.if_not_in_context if isinstance(self.if_not_in_context, list) else [self.if_not_in_context]
        result = all(path not in context for path in req)
        return self.executable_by_condition(result)


ContextActions = Union[tuple(ContextAction.__subclasses__())]  # pyright: ignore


###
### Executables, actions, choices, sequences, and workflows
###


class ExecModel(ContextModel):
    #: You can override name and description in the config (for purposes of choosing by LLM)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    #: What action or workflow to run next?
    #  Consider using a sequence (workflow) if you need to run multiple actions,
    #  to avoid nesting too deeply.
    # This also does not make sense in a sequence, so not sure if I should even include it
    # next: Optional[Executable] = Field(default=None)


class IterableExecModel(ExecModel):
    #: Iterate over a list of values (path string to a context variable) or a number of times (int)
    iterate: Union[int, ContextVarPath]

    #: What to name the iteration variable in the context
    as_: Optional[str] = Field(None, alias="as")

    #: Whether to allow allow finishing iteration early (include "Finished" as an action)
    allow_finish_early: bool = False

    # Ensure `as` is used with a varpath `iterate`
    @pydantic.validator("as_")
    def as_only_with_iterate(cls, v, values):
        if v is None and isinstance(values["iterate"], ContextVarPath):
            raise ValueError(f"`as` must be specified when `iterate` is a context variable path ({values['iterate']})")
        return v


class ActionConfig(ExecModel):
    action: ExecutableId
    inputs: Optional[ExtraModel] = None  # [str, ValueDeclaration]
    outputs: Optional[ExtraModel] = None  # [str, ContextVarName]


class IterableActionConfig(IterableExecModel):
    action: ExecutableId
    inputs: Optional[ExtraModel] = None  # [str, ValueDeclaration]
    list_outputs: Optional[ExtraModel] = None  # [str, ContextVarName]


# Builds action models from currently defined actions,


def build_actions():
    # Dynamically build action models from currently defined actions
    # for best typehints and autocompletion possible in the jsonschema

    def _templatify_model(
        model: type[pydantic.BaseModel],
        field_type: Optional[type] = None,
        add_union: Optional[type] = None,
        all_optional: bool = False
    ) -> tuple[type[pydantic.BaseModel], Any]:
        # Create a new model, put in a field of "field_type" for each input
        template_fields = {}
        for name_, field_ in model.__fields__.items():
            # Get the type of the field, which may be different in context than in the action
            type_ = field_.outer_type_

            # Transform it if so annotated
            if isinstance(type_, type) and issubclass(type_, TransformsFrom):
                type_ = type_._get_config_type()

            # Annotate optional fields with a default of None
            if all_optional or not field_.required:
                default = None
            else:
                default = ...
            template_field = Field(
                default=default,
                alias=field_.alias,
            )
            if field_type is not None:
                type_ = field_type
            if add_union is not None:
                # check that union does not collide with existing type
                if (
                    isinstance(type_, type) and
                    typing.get_origin(type_) is None and
                    issubclass(type_, pydantic.BaseModel)
                ):
                    for field_name in type_.__fields__.keys():
                        if any(field_name in m.__fields__
                               for m in typing.get_args(add_union)):
                            raise ValueError(
                                f"{field_name} is a restricted field name."
                            )
                # TODO if it's a template, enforce dict structure on the template
                type_ = Union[type_, add_union]
            template_fields[name_] = (type_, template_field)
        inputs_template = pydantic.create_model(
            action.id + model.__name__ + "ActionFieldTemplate",
            __base__=StrictModel,
            __module__=__name__,
            **template_fields,
        )
        inputs_template.update_forward_refs()

        # Annotate with a good default for the inputs themselves,
        # given if any of the inputs are required
        if not all_optional and any(
            f.required for f in model.__fields__.values()
        ):
            default = ...
        else:
            default = {}

        return inputs_template, default

    actions = get_actions_dict()
    action_models = []
    for action in actions.values():
        # build input fields
        fields = {
            "action": (Literal[action.id], ...)  # type: ignore
        }
        inputs = action._get_inputs_type()
        outputs = action._get_outputs_type()
        if not isinstance(None, inputs):
            input_fields = _templatify_model(inputs, add_union=ValueDeclaration)
        else:
            input_fields = (type(None), None)
        fields |= {
            "inputs": input_fields
        }

        # build output fields
        if not isinstance(None, outputs):
            output_fields = _templatify_model(outputs, field_type=ContextVarName, all_optional=True)
        else:
            output_fields = (type(None), None)
        invocation_fields = fields | {
            "outputs": output_fields
        }
        iterable_invocation_fields = fields | {
            "list_outputs": output_fields
        }

        # build action invocation model
        action_basemodel = pydantic.create_model(
            action.id + "ActionModel",
            __base__=ActionConfig,
            __module__=__name__,
            **invocation_fields,  # pyright: ignore[reportGeneralTypeIssues]
        )
        action_models.append(action_basemodel)
        # build iterable action invocation model
        iterable_action_basemodel = pydantic.create_model(
            action.id + "IterableActionModel",
            __base__=IterableActionConfig,
            __module__=__name__,
            **iterable_invocation_fields,  # pyright: ignore[reportGeneralTypeIssues]
        )
        action_models.append(iterable_action_basemodel)
    return action_models


ActionConfigs = Union[tuple(build_actions())]  # pyright: ignore

# Structures that require input values and return output values
# (e.g. for invoking workflows, or making a choice)


class IOValuesModel(ExecModel):
    #: Parses template string into the input, and passes it to the executable
    inputs: Optional[ExtraModel] = Field(default=None)

    #: What to name the output values in the context
    outputs: Optional[ExtraModel] = Field(default=None)


class IterableIOValuesModel(IterableExecModel):
    #: Parses template string into the input, and passes it to the executable
    inputs: Optional[ExtraModel] = Field(default=None)

    #: What to name the output values in the context
    list_outputs: Optional[ExtraModel] = Field(default=None)


class WorkflowInvocation(IOValuesModel):
    workflow: ExecutableId


class IterableWorkflowInvocation(IterableIOValuesModel):
    workflow: ExecutableId


# class Choice(IOValuesModel):
#     choose: list[Executable]


# Structures that specify what inputs and outputs they require and return



class IOSpecModel(ExecModel):
    #: Specifies what inputs the executable requires
    inputs: Optional[list[ContextVarName]] = Field(default=None)

    #: Specifies what outputs the executable returns
    outputs: Optional[list[ContextVarName]] = Field(default=None)


class WorkflowDefinition(IOSpecModel):
    steps: list[Executable]


ExecModel.update_forward_refs()
# Choice.update_forward_refs()
WorkflowInvocation.update_forward_refs()
WorkflowDefinition.update_forward_refs()
IfLambda.update_forward_refs()
IfContextNotExists.update_forward_refs()
IfExistsContext.update_forward_refs()
StrictModel.update_forward_refs()
SetVars.update_forward_refs()
ContextModel.update_forward_refs()
IOSpecModel.update_forward_refs()
IOValuesModel.update_forward_refs()
# TopLevelConfig.update_forward_refs()
IfLambda.update_forward_refs()
IfExistsContext.update_forward_refs()
IfContextNotExists.update_forward_refs()
for action in ExecModel.__subclasses__():
    action.update_forward_refs()
for action in IOSpecModel.__subclasses__():
    action.update_forward_refs()
for action in IOValuesModel.__subclasses__():
    action.update_forward_refs()
for action in ContextModel.__subclasses__():
    action.update_forward_refs()
ActionConfig.update_forward_refs()
for action in ActionConfig.__subclasses__():
    action.update_forward_refs()


TopLevelWorkflowConfig = dict[ExecutableId, WorkflowDefinition]

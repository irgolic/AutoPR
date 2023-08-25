import copy
import json
import typing
from typing import Any, Union, Optional, Literal, ForwardRef

import pydantic
from pydantic import Field

from autopr.actions.base import get_actions_dict, Action as ActionBase
from autopr.models.config.elements import ExecModel, ActionConfig, TopLevelWorkflowConfig, StrictModel, \
    WorkflowInvocation, IterableWorkflowInvocation, IOSpecModel, WorkflowDefinition, IfLambda, IfContextNotExists, \
    IfExistsContext, SetVars, ContextModel, IOValuesModel, ActionConfigs, ContextActions, ValueDeclaration
from autopr.models.events import EventUnion, LabelEvent, CommentEvent, PushEvent

from autopr.models.executable import LambdaString, ContextVarPath, ExecutableId, Executable, \
    TemplateObject, ContextVarName, ContextDict, StrictExecutable
from autopr.workflows import get_all_workflows


###
### For strict config, build workflow definitions
###


def build_workflows():
    # Dynamically build workflow models from currently defined workflows
    # for best typehints and autocompletion possible in the jsonschema
    workflows: TopLevelWorkflowConfig = get_all_workflows()
    workflow_models = []
    for workflow_id, workflow in workflows.items():
        fields = {
            "workflow": (Literal[workflow_id], ...)  # type: ignore
        }
        if workflow.inputs is not None:
            input_fields_model = pydantic.create_model(
                workflow_id + "Inputs",
                __base__=StrictModel,
                __module__=__name__,
                **{
                    name: (ValueDeclaration, Field(default=...))
                    for name in workflow.inputs
                },  # pyright: ignore[reportGeneralTypeIssues]
            )
            input_fields = (input_fields_model, ...)
        else:
            input_fields = (type(None), None)
        fields |= {
            "inputs": input_fields
        }

        if workflow.outputs is not None:
            output_fields_model = pydantic.create_model(
                workflow_id + "Outputs",
                __base__=StrictModel,
                __module__=__name__,
                **{
                    name: (Optional[ContextVarName], Field(default=None))
                    for name in workflow.outputs
                },  # pyright: ignore[reportGeneralTypeIssues]
            )
            output_fields = (output_fields_model, None)
        else:
            output_fields = (type(None), None)
        invocation_fields = fields | {
            "outputs": output_fields
        }
        iterable_invocation_fields = fields | {
            "list_outputs": output_fields
        }

        # build workflow invocation model
        workflow_basemodel = pydantic.create_model(
            workflow_id + "WorkflowModel",
            __base__=WorkflowInvocation,
            __module__=__name__,
            **invocation_fields,  # pyright: ignore[reportGeneralTypeIssues]
        )
        workflow_models.append(workflow_basemodel)

        # build iterable workflow invocation model
        iterable_workflow_basemodel = pydantic.create_model(
            workflow_id + "IterableWorkflowModel",
            __base__=IterableWorkflowInvocation,
            __module__=__name__,
            **iterable_invocation_fields,  # pyright: ignore[reportGeneralTypeIssues]
        )
        workflow_models.append(iterable_workflow_basemodel)

    return workflow_models


WorkflowInvocationConfigs = Union[tuple(ws)] if (ws := build_workflows()) else None  # pyright: ignore


def get_all_executable_ids():
    ids = []

    actions = get_actions_dict()
    ids.extend(actions.keys())

    workflows = get_all_workflows()
    ids.extend(workflows.keys())

    return ids


StrictExecutableId = Literal[tuple(ids_)] if (ids_ := get_all_executable_ids()) else None  # pyright: ignore


###
### Triggers (labels, comment substrings)
###


class TriggerModel(ContextModel):
    type: str
    run: StrictExecutable = Field()  # pyright: ignore[reportGeneralTypeIssues]
    parameters: Optional[dict[str, Any]] = Field(default=None)

    def get_context_for_event(self, event: EventUnion) -> Optional[ContextDict]:
        raise NotImplementedError


class LabelTrigger(TriggerModel):
    type: Literal["label"] = "label"
    label_substring: str
    on_issue: bool
    on_pull_request: bool

    def get_context_for_event(self, event: EventUnion) -> Optional[ContextDict]:
        if (
            isinstance(event, LabelEvent) and
            self.label_substring.lower() in event.label.lower() and
            (
                self.on_pull_request and event.pull_request is not None or
                self.on_issue and not event.pull_request is not None
            )
        ):
            return ContextDict(
                issue=event.issue,
                pull_request=event.pull_request,
            )
        return None


class CommentTrigger(TriggerModel):
    type: Literal["comment"] = "comment"
    comment_substring: str
    on_issue: bool
    on_pull_request: bool

    def get_context_for_event(self, event: EventUnion) -> Optional[ContextDict]:
        if (
            isinstance(event, CommentEvent) and
            self.comment_substring.lower() in event.comment.body.lower()
        ):
            return ContextDict(
                issue=event.issue,
                pull_request=event.pull_request,
            )
        return None


class PushTrigger(TriggerModel):
    type: Literal["push"] = "push"
    branch_name: str

    def get_context_for_event(self, event: EventUnion) -> Optional[ContextDict]:
        if (
            isinstance(event, PushEvent) and
            self.branch_name == event.branch
        ):
            return ContextDict(
                issue=event.issue,
                pull_request=event.pull_request,
            )
        return None


Trigger = Union[LabelTrigger, CommentTrigger, PushTrigger]


###
### Parsing entrypoints
###


class StrictWorkflowDefinition(IOSpecModel):
    steps: list[StrictExecutable]  # pyright: ignore[reportGeneralTypeIssues]


StrictTopLevelWorkflowConfig = dict[ExecutableId, StrictWorkflowDefinition]


class TopLevelTriggerConfig(StrictModel):
    triggers: list[Trigger] = Field(default_factory=list)  # pyright: ignore[reportGeneralTypeIssues]


StrictWorkflowDefinition.update_forward_refs()

trigger_schema = pydantic.schema_json_of(TopLevelTriggerConfig)
workflow_schema = pydantic.schema_json_of(TopLevelWorkflowConfig)
strict_workflow_schema = pydantic.schema_json_of(StrictTopLevelWorkflowConfig)

if __name__ == '__main__':
    with open("trigger_schema.json", "w") as f:
        json.dump(json.loads(trigger_schema), f, indent=2)
    with open("workflow_schema.json", "w") as f:
        json.dump(json.loads(workflow_schema), f, indent=2)
    with open("strict_workflow_schema.json", "w") as f:
        json.dump(json.loads(strict_workflow_schema), f, indent=2)

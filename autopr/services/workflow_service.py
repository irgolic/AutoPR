import asyncio
import glob
import itertools
import json
import typing
from typing import Coroutine, Any, Union, Optional, Iterable

import jinja2
import pydantic

from autopr.actions.base import get_actions_dict, Action
from autopr.log_config import get_logger
from autopr.models.config.elements import Executable, ContextAction, ActionConfig, WorkflowDefinition, \
    WorkflowInvocation, IterableActionConfig, IterableWorkflowInvocation, ValueDeclaration
from autopr.models.config.entrypoints import TopLevelWorkflowConfig, Trigger
from autopr.models.events import EventUnion
from autopr.models.executable import ExecutableId, ContextDict, TemplateObject
from autopr.services.action_service import ActionService
from autopr.services.publish_service import PublishService
from autopr.services.utils import truncate_strings, format_for_publishing


class WorkflowService:
    def __init__(
        self,
        workflows: TopLevelWorkflowConfig,
        triggers: list[Trigger],
        action_service: ActionService,
        publish_service: PublishService,
        strict: bool = True,
    ):
        self.workflows = workflows
        self.triggers = triggers
        self.action_service = action_service
        self.publish_service = publish_service
        self.strict = strict

        print("Loaded triggers:")
        for t in self.triggers:
            print(t.json(indent=2))

        self.log = get_logger(service="workflow")

    def _get_name_for_executable(self, executable: Executable) -> str:
        if isinstance(executable, str):
            return executable
        if isinstance(executable, ActionConfig):
            return executable.action
        if isinstance(executable, WorkflowInvocation) or isinstance(executable, IterableWorkflowInvocation):
            return executable.workflow
        if isinstance(executable, ContextAction):
            raise RuntimeError("Meaningless trigger! Whatchu tryina do :)")
        raise ValueError(f"Unknown executable type {executable}")

    async def _get_trigger_coros_for_event(self, event: EventUnion) -> list[Coroutine[Any, Any, ContextDict]]:
        # Gather all triggers that match the event
        triggers_and_context: list[tuple[Trigger, ContextDict]] = []
        for trigger in self.triggers:
            context = trigger.get_context_for_event(event)
            if context is None:
                continue
            triggers_and_context.append((trigger, context))

        # Build coroutines for each trigger
        if not triggers_and_context:
            return []
        if len(triggers_and_context) == 1:
            self.publish_service.title = f"AutoPR: {self._get_name_for_executable(triggers_and_context[0][0].run)}"
            return [
                self.handle_trigger(
                    trigger,
                    context,
                    publish_service=self.publish_service,
                )
                for trigger, context in triggers_and_context
            ]
        trigger_titles = [self._get_name_for_executable(trigger.run) for trigger, context in triggers_and_context]
        self.publish_service.title = f"AutoPR: {', '.join(truncate_strings(trigger_titles))}"
        return [
            self.handle_trigger(
                trigger,
                context,
                publish_service=(await self.publish_service.create_child(title=title)),
            )
            for i, ((trigger, context), title) in enumerate(zip(triggers_and_context, trigger_titles))
        ]

    async def trigger_event(
        self,
        event: EventUnion,
    ):
        triggers = await self._get_trigger_coros_for_event(event)
        if not triggers:
            print(event)
            self.log.debug(f"No triggers for event")
            return

        results = await asyncio.gather(*triggers)

        exceptions = []
        for r in results:
            if isinstance(r, Exception):
                self.log.error("Error in trigger", exc_info=r)
                exceptions.append(r)

        if exceptions:
            await self.publish_service.finalize(False, exceptions)
        else:
            await self.publish_service.finalize(True)

        return results

    def get_executable_by_id(self, id_: ExecutableId, context: ContextDict) -> Union[ActionConfig, WorkflowDefinition]:
        # Look in actions
        action = self.action_service.find_action(id_)
        if action is not None:
            # Build action config
            inputs_type = action._get_inputs_type()
            if inputs_type is None:
                return ActionConfig(action=id_)

            # Build inputs dict from context named the same as the inputs
            inputs_dict = {}
            for field_name, field in inputs_type.__fields__.items():
                # Check if all required inputs are present in context
                if field_name in context:
                    inputs_dict[field_name] = context[field_name]
                elif field.required:
                    raise ValueError(f"Missing required input `{field_name}` for action `{id_}`")

            return ActionConfig(
                action=id_,
                inputs=inputs_type(**inputs_dict),
            )
        # Look in workflows
        for workflow_id, workflow_definition in self.workflows.items():
            if workflow_id == id_:
                return workflow_definition
        raise ValueError(f"Could not find executable with id `{id_}`")

    async def execute_by_id(
        self,
        id_: ExecutableId,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        executable = self.get_executable_by_id(id_, context)
        if isinstance(executable, ActionConfig):
            return await self.action_service.run_action(executable, context, publish_service)
        if isinstance(executable, WorkflowDefinition):
            return await self.publish_and_execute_workflow(id_, executable, context, publish_service)
        raise ValueError(f"`{id_}` is not an executable")

    def _prepare_workflow_inputs(
        self,
        inputs: Optional[pydantic.BaseModel],  # [str, TemplateObject]
        context: ContextDict,
    ):
        # Pass __params__ through
        input_values = {
            k: v
            for k, v in context.items()
            if k.startswith("__") and k.endswith("__")
        }

        if inputs is None:
            return ContextDict(input_values)

        for key, template in inputs:

            # Try to parse as ValueDeclaration Union
            try:
                template = pydantic.parse_obj_as(ValueDeclaration, template)
            except pydantic.ValidationError:
                pass

            if any(isinstance(template, t) for t in typing.get_args(ValueDeclaration)):
                input_values[key] = template.render(context)
            else:
                input_values[key] = context.render_nested_template(template)

        return ContextDict(input_values)

    async def publish_and_execute_workflow(
        self,
        workflow_id: ExecutableId,
        workflow_definition: WorkflowDefinition,
        input_context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        await publish_service.start_section(f"🌊 Invoking `{workflow_id}`")

        context = await self.execute_workflow(workflow_definition, input_context, publish_service)

        await publish_service.end_section(f"🌊 Invoked `{workflow_id}`")
        return context

    async def invoke_workflow(
        self,
        workflow_invocation: WorkflowInvocation,
        context: ContextDict,
        publish_service: PublishService,
    ):
        # Prepare inputs
        input_context = self._prepare_workflow_inputs(workflow_invocation.inputs, context)

        # Execute workflow
        workflow_definition = self.get_executable_by_id(workflow_invocation.workflow, input_context)
        if not isinstance(workflow_definition, WorkflowDefinition):
            raise ValueError(f"`{workflow_invocation.workflow}` is not a workflow")
        context = await self.publish_and_execute_workflow(workflow_invocation.workflow,
                                                          workflow_definition,
                                                          input_context,
                                                          publish_service)

        # Grab outputs
        output_context = ContextDict()
        if workflow_invocation.outputs:
            src = workflow_invocation.outputs.dict()
        else:
            src = {}
        for output, varname in src.items():
            output_context[varname] = context[output]

        return output_context

    async def invoke_workflow_iteratively(
        self,
        iter_workflow_invocation: IterableWorkflowInvocation,
        context: ContextDict,
        publish_service: PublishService,
    ):
        await publish_service.start_section(f"🌳 Iteratively invoking `{iter_workflow_invocation.workflow}`")

        executable = self.get_executable_by_id(iter_workflow_invocation.workflow, context)
        if isinstance(executable, ActionConfig):
            raise ValueError("Executable is an action, not a workflow")

        iteration = iter_workflow_invocation.iterate
        if isinstance(iteration, int):
            # iterate workflow `iteration` times
            item_name = iter_workflow_invocation.as_
            iter_context = context
            coros = []
            for i in range(iteration):
                # Prepare inputs
                if item_name is not None:
                    iter_context = ContextDict(iter_context | {item_name: i})
                input_context = self._prepare_workflow_inputs(
                    iter_workflow_invocation.inputs,
                    iter_context,
                )
                # Prepare coroutine
                coros.append(self.execute_workflow(
                    executable,
                    input_context,
                    await publish_service.create_child(title=f"🌊 Iteration {i + 1}"),
                ))
        else:  # isinstance(iteration, ContextVarPath)
            # iterate over a list in the context
            list_var = context.get_path(iteration)
            if not isinstance(list_var, Iterable):
                raise ValueError(f"Expected {iteration} to be an iterable")

            # Get inputs including the list item
            item_name = iter_workflow_invocation.as_
            if item_name is None:
                raise ValueError("Expected `as` to be specified for workflow iterating over a list")

            coros = []
            for item in list_var:
                # Prepare inputs
                iter_context = ContextDict(context | {item_name: item})
                input_context = self._prepare_workflow_inputs(
                    iter_workflow_invocation.inputs,
                    iter_context,
                )
                # Prepare coroutine
                coros.append(self.execute_workflow(
                    executable,
                    input_context,
                    await publish_service.create_child(
                        title=f"🌊 Iteration: `{truncate_strings(str(item), length=40)}`"
                    ),
                ))

        # Run all coroutines in parallel
        output_contexts = await asyncio.gather(*coros)

        await publish_service.end_section(f"🌳 Iteratively invoked `{iter_workflow_invocation.workflow}`")

        # Grab outputs
        output_context = ContextDict()
        if iter_workflow_invocation.list_outputs:
            src = iter_workflow_invocation.list_outputs.dict()
        else:
            src = {}
        for output, varname in src.items():
            output_context[varname] = [c[output] for c in output_contexts]

        await publish_service.publish_code_block(
            heading="Outputs",
            code=format_for_publishing(output_context),
            language="json",
        )

        return output_context
    
    def validate_workflow_inputs_and_outputs(self, inputs_outputs_list, context, workflow):
        """Validates that all inputs and outputs are present in the inputs_outputs_list.
        This method is used for validating inputs and outputs of the workflow."""
        for element in inputs_outputs_list:
            if element in context:
                continue
            error_suffix = f' `{workflow.name}`' if workflow.name else ''
            error_msg = f"Missing input `{element}` for workflow{error_suffix}"
            if self.strict:
                raise ValueError(error_msg)
            else:
                self.log.warn(error_msg)

    async def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        await publish_service.publish_code_block(
            heading="Inputs",
            code=format_for_publishing(context),
            language="json",
        )

        # Check if inputs in signature are present in the passed context
        inputs = workflow.inputs or []
        self.validate_workflow_inputs_and_outputs(inputs, context, workflow)

        # Execute steps in order
        for executable in workflow.steps:
            context = await self.execute(executable, context, publish_service)

        # Check if outputs are present
        outputs = workflow.outputs or []
        self.validate_workflow_inputs_and_outputs(outputs, context, workflow)

        # Grab outputs
        output_context = ContextDict()
        for output in outputs:
            if isinstance(output, str):
                name = output
            else:  # isinstance(output, VarSpec)
                name = output.name
            output_context[name] = context[name]

        await publish_service.publish_code_block(
            heading="Outputs",
            code=format_for_publishing(output_context),
            language="json",
        )

        return output_context

    async def handle_trigger(
        self,
        trigger: Trigger,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        await publish_service.publish_code_block(
            heading="📣 Trigger",
            code=format_for_publishing(trigger),
            language="json",
        )
        await publish_service.publish_code_block(
            heading="🎬 Starting context",
            code=format_for_publishing(context),
            language="json",
        )

        executable = trigger.run

        # Add params
        if trigger.parameters:
            context["__params__"] = trigger.parameters

        try:
            context = await self.execute(
                executable,
                context,
                publish_service=publish_service,
            )
        except Exception as e:
            self.log.error("Error while executing", executable=executable, exc_info=e)
            raise

        await publish_service.publish_code_block(
            heading="🏁 Final context",
            code=format_for_publishing(context),
            language="json",
        )

        return context

    async def execute(
        self,
        executable: Executable,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        if isinstance(executable, list):
            for e in executable:
                context = await self.execute(e, context, publish_service)
            output_context = context
        elif isinstance(executable, str):
            output_context = await self.execute_by_id(ExecutableId(executable), context, publish_service)
        elif isinstance(executable, ContextAction):
            executable = executable.get_executable(context)
            if executable is None:
                return context
            output_context = await self.execute(executable, context, publish_service)
        elif isinstance(executable, ActionConfig):
            output_context = await self.action_service.run_action(executable, context, publish_service)
        elif isinstance(executable, IterableActionConfig):
            output_context = await self.action_service.run_action_iteratively(executable, context, publish_service)
        elif isinstance(executable, WorkflowInvocation):
            output_context = await self.invoke_workflow(executable, context, publish_service)
        elif isinstance(executable, IterableWorkflowInvocation):
            output_context = await self.invoke_workflow_iteratively(executable, context, publish_service)
        # elif isinstance(executable, Choice):
        #     output_context = await self.action_service.run_actions_iteratively(executable.choose, context)
        else:
            raise TypeError(f"Unknown executable type {type(executable)}")

        # Merge outputs with existing context
        context.update(output_context)
        return context

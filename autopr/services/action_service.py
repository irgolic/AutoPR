import asyncio
import json
import traceback
import typing
from typing import Any, Optional, Collection, Type, TypeVar, Iterable

import jinja2
import pydantic
from git.repo import Repo
from pydantic import ValidationError, BaseModel

from autopr.actions.base import get_actions_dict, Action, Outputs, Inputs
from autopr.log_config import get_logger
from autopr.models.config.transform import TransformsInto
from autopr.models.executable import ContextDict, ExecutableId

from autopr.models.config.elements import ActionConfig, IterableActionConfig, ValueDeclaration
from autopr.services.cache_service import CacheService, ShelveCacheService
from autopr.services.commit_service import CommitService
from autopr.services.platform_service import PlatformService
from autopr.services.publish_service import PublishService
from autopr.services.utils import truncate_strings, format_for_publishing

ActionSubclass = Action[Any, Any]


class ActionService:
    # class Finished(Action):
    #     id = "finished"

    def __init__(
        self,
        repo: Repo,
        config_dir: str,
        platform_service: PlatformService,
        commit_service: CommitService,
        num_reasks: int = 3
    ):
        self.repo = repo
        self.config_dir = config_dir
        self.platform_service = platform_service
        self.commit_service = commit_service
        self.num_reasks = num_reasks

        # Load all actions in the `autopr/actions` directory
        self.actions: dict[ExecutableId, type[ActionSubclass]] = get_actions_dict()

        self.log = get_logger(service="action_service")

    def find_action(self, id_: ExecutableId) -> Optional[type[Action[Any, Any]]]:
        if id_ in self.actions:
            return self.actions[id_]
        return None

    def instantiate_action(
        self,
        action_type: Type[Action[Inputs, Outputs]],
        publish_service: PublishService,
    ) -> Action[Inputs, Outputs]:
        cache_service = ShelveCacheService(
            config_dir=self.config_dir,
            action_id=action_type.id,
        )
        return action_type(
            repo=self.repo,
            publish_service=publish_service,
            platform_service=self.platform_service,
            commit_service=self.commit_service,
            cache_service=cache_service,
        )

    def get_action_inputs(
        self,
        action_type: Type[Action[Inputs, Outputs]],
        action_inputs: Inputs,
        context: ContextDict,
    ) -> Optional[Inputs]:
        # Get the inputs
        inputs_type = action_type._get_inputs_type()
        if isinstance(None, inputs_type):
            inputs = None
        else:
            if action_inputs is None:
                specified_inputs = {}
            else:
                specified_inputs = action_inputs

            input_values = {}
            for input_name, template in specified_inputs:
                # resolve prompt contexts
                if isinstance(template, TransformsInto):
                    template = template.transform_from_config(template, context)
                # resolve variable declarations
                elif any(isinstance(template, t) for t in typing.get_args(ValueDeclaration)):
                    template = template.render(context)
                # resolve string as template (backwards compatibility, should be removed)
                elif isinstance(template, str):
                    template = context.render_nested_template(template)

                if isinstance(template, pydantic.BaseModel):
                    template = template.dict()

                if template is not None:
                    input_values[input_name] = template

            try:
                inputs = inputs_type(**input_values)  # pyright: ignore[reportGeneralTypeIssues]
            except ValidationError as e:
                raise ValueError(
                    f"Invalid inputs for {action_type.id}:\n\n{e}"
                ) from e

        return inputs

    async def _instantiate_and_run_action(
        self,
        action_type: Type[Action[Inputs, Outputs]],
        action_id: str,
        inputs: Inputs,
        publish_service: PublishService,
    ):
        if inputs is not None:
            formatted_inputs = format_for_publishing(inputs)
        else:
            formatted_inputs = "None"
        await publish_service.publish_code_block("Inputs", formatted_inputs, language="json")

        # Instantiate the action
        action = self.instantiate_action(
            action_type=action_type,
            publish_service=publish_service,
        )

        # Run the action
        try:
            outputs = await action.run(inputs)
        except Exception:
            self.log.exception(f"Failed to run action {action_id}")
            await publish_service.publish_code_block(
                heading="Error",
                code=traceback.format_exc(),
                language="python",  # FIXME
                                    #  does nice syntax highlighting for tracebacks, but should be made configurable
            )
            await publish_service.end_section(f"❌ Failed {action_id}")
            raise

        return outputs

    async def run_action(
        self,
        action_config: ActionConfig,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        action_id = action_config.action
        section_title = f"💧 Running `{action_id}`"
        await publish_service.start_section(section_title)

        action_type = self.actions[action_id]

        # Get inputs
        inputs = self.get_action_inputs(action_type, action_config.inputs, context)

        # Run action
        outputs = await self._instantiate_and_run_action(
            action_type=action_type,
            action_id=action_id,
            inputs=inputs,
            publish_service=publish_service,
        )

        if outputs is not None:
            # Publish raw outputs
            await publish_service.publish_code_block(
                "Outputs",
                format_for_publishing(outputs),
                language="json",
            )

        # Extract outputs
        new_context = {
            context_key: getattr(outputs, output_name)
            for output_name, context_key in action_config.outputs or {}
            if context_key is not None
        }
        
        if new_context:
            # Publish outputs
            await publish_service.publish_code_block(
                "New Variables",
                format_for_publishing(new_context),
                language="json",
            )

        # End the section
        if publish_service.sections_stack[-1].title == section_title:
            await publish_service.end_section(f"💧 Finished running `{action_id}`")
        else:
            await publish_service.end_section()

        return ContextDict(new_context)

    async def run_action_iteratively(
        self,
        iter_action_config: IterableActionConfig,
        context: ContextDict,
        publish_service: PublishService,
    ) -> ContextDict:
        action_id = iter_action_config.action
        section_title = f"💦 Iteratively running `{action_id}`"
        await publish_service.start_section(section_title)

        action_type = self.actions[action_id]

        iteration = iter_action_config.iterate
        if isinstance(iteration, int):
            # iterate `iteration` times
            item_name = iter_action_config.as_
            iter_context = context
            coros = []
            for i in range(iteration):
                if item_name is not None:
                    iter_context = ContextDict(iter_context | {item_name: i})

                # Get inputs
                inputs = self.get_action_inputs(action_type, iter_action_config.inputs, iter_context)

                coros.append(self._instantiate_and_run_action(
                    action_type=action_type,
                    action_id=action_id,
                    inputs=inputs,
                    publish_service=await publish_service.create_child(f"💧 Iteration {i+1}"),
                ))
        else:  # isinstance(iteration, ContextVarPath)
            # iterate over a list in the context
            list_var = context.get_path(iteration)
            if not isinstance(list_var, Iterable):
                raise ValueError(f"Expected {iteration} to be an iterable")

            # Get inputs including the list item
            item_name = iter_action_config.as_
            if item_name is None:
                raise ValueError("Expected `as` to be specified for action iterating over a list")
            coros = []
            for item in list_var:
                iter_context = ContextDict(context | {item_name: item})
                inputs = self.get_action_inputs(action_type, iter_action_config.inputs, iter_context)
                coros.append(self._instantiate_and_run_action(
                    action_type=action_type,
                    action_id=action_id,
                    inputs=inputs,
                    publish_service=await publish_service.create_child(
                        title=f"💧 Iteration: `{truncate_strings(str(item), length=40)}`"
                    ),
                ))

        # Gather the action runs
        outputses = await asyncio.gather(*coros)

        # Extract outputs
        new_context = {}
        for output_name, context_key in iter_action_config.list_outputs or {}:
            if context_key is None:
                continue
            new_context[context_key] = [
                getattr(outputs, output_name)
                for outputs in outputses
            ]

        await publish_service.publish_code_block(
            "Outputs",
            format_for_publishing(new_context),
            language="json",
        )

        # End the section
        if publish_service.sections_stack[-1].title == section_title:
            await publish_service.end_section(f"💦 Finished iterating `{action_id}`")
        else:
            await publish_service.end_section()

        return ContextDict(new_context)

from typing import Optional, Collection, Type

import pydantic
import structlog
from git.repo import Repo

from autopr.actions.base import get_all_actions, Action

from autopr.actions.base import ContextDict
from autopr.models.rail_objects import RailObject
from autopr.repos.completions_repo import CompletionsRepo
from autopr.services.chain_service import ChainService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService


class ActionService:
    def __init__(
        self,
        repo: Repo,
        completions_repo: CompletionsRepo,
        publish_service: PublishService,
        rail_service: RailService,
        chain_service: ChainService,
        num_reasks: int = 3
    ):
        self.repo = repo
        self.completions_repo = completions_repo
        self.publish_service = publish_service
        self.rail_service = rail_service
        self.chain_service = chain_service
        self.num_reasks = num_reasks

        # Load all actions in the `autopr/actions` directory
        self.actions: dict[str, type[Action]] = {
            action.id: action
            for action in get_all_actions()
        }

        self.log = structlog.get_logger(service="action_service")

    def _write_action_selection_rail_spec(
        self,
        action_ids: Collection[str],
    ) -> str:
        # Write the "choice" output spec
        output_spec = f"""<choice
            name="action"
            on-fail-choice="reask"
        >"""
        for action_id in action_ids:
            action = self.actions[action_id]
            case_spec = f"""<case
                name="{action.id}"
                {f'description="{action.description}"' if action.description else ""}
            >"""
            if action.Arguments.output_spec:
                case_spec += f"""<object
                    name="{action.id}"
                >
                {action.Arguments.output_spec}
                </object>"""
            case_spec += f"""</case>"""
            output_spec += case_spec
        output_spec += f"""<case
            name="finished"
        >
        </case>
        </choice>"""

        # Wrap it in a rail spec
        return f"""
<rail version="0.1">
<output>
{output_spec}
</output>
<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

@json_suffix_prompt_examples
</instructions>
<prompt>
{{{{context}}}}

You are about to make a decision on what to do next, and return a JSON that follows the correct schema.

@xml_prefix_prompt

{{output_schema}}
</prompt>
</rail>
"""

    @staticmethod
    def _write_action_args_query_rail_spec(
        arguments: Type[Action.Arguments],
    ) -> str:
        return f"""
<rail version="0.1">
<output>
{arguments.output_spec}
</output>
<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

@json_suffix_prompt_examples
</instructions>
<prompt>
{{{{context}}}}

You are about to make a decision on what to do next, and return a JSON that follows the correct schema.

@xml_prefix_prompt

{{output_schema}}
</prompt>
</rail>
"""

    def instantiate_action(
        self,
        action_type: Type[Action],
    ):
        return action_type(
            repo=self.repo,
            rail_service=self.rail_service,
            chain_service=self.chain_service,
            publish_service=self.publish_service,
        )

    def run_action(
        self,
        action_id: str,
        context: ContextDict,
    ) -> ContextDict:
        # Get the action
        action_type = self.actions[action_id]

        # If the action defines arguments, ask the LLM to fill them in
        if action_type.Arguments is not Action.Arguments:
            # Ask the LLM to fill in the arguments
            arguments = self.ask_for_action_arguments(
                action_type=action_type,
                context=context,
            )
            if arguments is None:
                self.log.error("Guardrails failed to specify action arguments")
                return context
        else:
            arguments = Action.Arguments()

        # Instantiate the action
        action = self.instantiate_action(action_type)

        # Run the action
        return action.run(arguments, context)

    def run_actions_iteratively(
        self,
        action_ids: Collection[str],
        context: ContextDict,
        max_iterations: int = 5,
    ) -> ContextDict:
        for _ in range(max_iterations):
            # Pick an action
            pick = self.pick_action(
                action_ids=action_ids,
                context=context,
            )
            if pick is None:
                break
            action_type, args = pick

            # Instantiate the action
            action = self.instantiate_action(action_type)

            # Run the action
            context = action.run(args, context)
        return context

    def ask_for_action_arguments(
        self,
        action_type: Type[Action],
        context: ContextDict,
    ) -> Optional[Action.Arguments]:
        if action_type.Arguments is Action.Arguments:
            # No arguments to fill in
            return Action.Arguments()

        # Generate the arguments query spec
        rail_spec = self._write_action_args_query_rail_spec(
            arguments=action_type.Arguments,
        )

        # Run the rail
        dict_o = self.rail_service.run_rail_string(
            rail_spec,
            prompt_params={
                "context": str(context),
            },
        )
        if dict_o is None:
            self.log.error("Guardrails failed to choose an action")
            return None

        # Parse the arguments
        try:
            args = action_type.Arguments.parse_obj(dict_o)
        except pydantic.ValidationError as e:
            self.log.error("Guardrails failed to parse action arguments", error=e)
            return None
        return args

    def pick_action(
        self,
        action_ids: Collection[str],
        context: ContextDict,
    ) -> Optional[tuple[type[Action], Action.Arguments]]:
        # Generate the action-select rail spec
        rail_spec = self._write_action_selection_rail_spec(
            action_ids=action_ids,
        )

        # Instantiate the rail
        dict_o = self.rail_service.run_rail_string(
            rail_spec,
            prompt_params={
                "context": str(context),
            },
        )
        if dict_o is None:
            self.log.error("Guardrails failed to choose an action")
            return None

        # Get the action
        action_id = dict_o["action"]
        if action_id == "finished":
            # Done!
            return None

        action_args_dict = dict_o.get(action_id, {})
        action = self.actions[action_id]
        args = action.Arguments.parse_obj(action_args_dict)
        return action, args

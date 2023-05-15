import traceback
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
    class Finished(Action):
        id = "finished"

        class Arguments(Action.Arguments):
            reason: str

            output_spec = """<string
                name="reason"
                required="true"
            />"""

        def run(self, arguments: Action.Arguments, context: ContextDict) -> ContextDict:
            return context

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
        include_finished: bool = False,
    ) -> str:
        # Add finished action
        if include_finished and "finished" not in action_ids:
            action_ids = [*action_ids, "finished"]
        # Write the "choice" output spec
        output_spec = f"""<choice
            name="action"
            on-fail-choice="reask"
        >"""
        for action_id in action_ids:
            action = self.actions[action_id]
            output_spec += f"""<case
                name="{action.id}"
                {f'description="{action.description}"' if action.description else ""}
            >"""
            if action.Arguments.output_spec:
                output_spec += f"""<object
                    name="{action.id}"
                >
                {action.Arguments.output_spec}
                </object>"""
            else:
                output_spec += """<string 
                    name="reason"
                />"""
            output_spec += f"""</case>"""
        output_spec += f"""</choice>"""

        # Wrap it in a rail spec
        return f"""
<rail version="0.1">
<output>
{output_spec}
</output>
<instructions>
You are AutoPR, an autonomous pull request creator and a helpful assistant only capable of communicating with valid JSON, and no other text.

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
You are AutoPR, an autonomous pull request creator and a helpful assistant only capable of communicating with valid JSON, and no other text.

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

        section_title = f"🚀 Running {action_id}"
        self.publish_service.start_section(section_title)

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
        try:
            results = action.run(arguments, context)
        except Exception:
            self.log.exception(f"Failed to run action {action_id}")
            self.publish_service.publish_code_block(
                heading="Error",
                code=traceback.format_exc(),
                language="python",  # FIXME
                                    #  does nice syntax highlighting for tracebacks, but should be made configurable
            )
            self.publish_service.end_section(f"❌ Failed {action_id}")
            raise

        if self.publish_service.sections_stack[-1].title == section_title:
            self.publish_service.end_section(f"✅ Finished {action_id}")
        self.publish_service.end_section()

        return results

    def run_actions_iteratively(
        self,
        action_ids: Collection[str],
        context: ContextDict,
        context_headings: Optional[dict[str, str]] = None,
        max_iterations: int = 5,
        include_finished: bool = False,
    ) -> ContextDict:
        for _ in range(max_iterations):
            if len(action_ids) == 1 and not include_finished:
                action_id = next(iter(action_ids))
                context = self.run_action(action_id, context)
                break

            self.publish_service.start_section("❓ Choosing next action")
            # Pick an action
            pick = self.pick_action(
                action_ids=action_ids,
                context=context,
                include_finished=include_finished,
                context_headings=context_headings,
            )
            if pick is None or pick[0].id == "finished":
                self.publish_service.end_section("🏁 No action chosen")
                break
            action_type, args = pick

            # Instantiate the action
            action = self.instantiate_action(action_type)

            self.publish_service.update_section(f"🚀 Running {action.id}")

            # Run the action
            context = action.run(args, context)

            self.publish_service.end_section()

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
                "context": context.as_string(),
            },
            heading="action arguments",
        )
        if dict_o is None:
            self.log.error("Guardrails failed to specify action arguments")
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
        include_finished: bool = False,
        context_headings: Optional[dict[str, str]] = None,
    ) -> Optional[tuple[type[Action], Action.Arguments]]:
        """
        Pick an action to run next.

        Returns a tuple of the action type and the arguments to instantiate it with.

        """
        # Generate the action-select rail spec
        rail_spec = self._write_action_selection_rail_spec(
            action_ids=action_ids,
            include_finished=include_finished,
        )
        self.log.debug("Wrote action-selection rail spec:\n%s", rail_spec=rail_spec)

        # Instantiate the rail
        dict_o = self.rail_service.run_rail_string(
            rail_spec,
            prompt_params={
                "context": context.as_string(
                    variable_headings=context_headings,
                ),
            },
            heading="action choice",
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

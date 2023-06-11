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

        self.actions: dict[str, type[Action]] = {
            action.id: action
            for action in get_all_actions()
        }

        self.log = structlog.get_logger(service="action_service")

    def _write_action_selection_rail_spec(
        self,
        action_ids: Collection[str],
        include_finished: bool = False,
        current_commit_index: int = None,
        current_commit_title: str = None,
    ) -> str:
        if include_finished and "finished" not in action_ids:
            action_ids = [*action_ids, "finished"]
        output_spec = f"""<choice
            name="action"
            on-fail-choice="reask"
        >"""
        for action_id in action_ids:
            action = self.actions[action_id]
            output_spec += f"""<case
                name="{action.id}"
                {f'description="{action.description}"' if action.description else ""}
            >
            <object
                name="{action.id}"
            >"""
            if action.Arguments.output_spec:
                output_spec += action.Arguments.output_spec
            else:
                if action.Arguments is not Action.Arguments:
                    raise ValueError(
                        f"{action.__name__}.Arguments ({action_id}) is missing an output spec"
                    )
                output_spec += """<string 
                    name="reason"
                />"""
            output_spec += f"""
            </object>
            """
            output_spec += f"""</case>"""
        output_spec += f"""</choice>"""

        return f"""
<rail version="0.1">
<output>
{output_spec}
</output>
<instructions>
You are AutoPR, an autonomous pull request creator and a helpful assistant only capable of communicating with valid JSON, and no other text.

@autopr_json_suffix_prompt_examples
</instructions>
<prompt>
{{{{context}}}}

You are about to make a decision on what to do next, and return a JSON that follows the correct schema.

{f'Current Commit ({current_commit_index}): {current_commit_title}' if current_commit_index is not None and current_commit_title is not None else ''}

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

@autopr_json_suffix_prompt_examples
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
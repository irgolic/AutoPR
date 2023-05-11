import json
import traceback
from typing import Callable, Any, Optional, TypeVar, Type

import pydantic

import guardrails as gr
from autopr.models.rail_objects import RailObject
from autopr.models.prompt_rails import PromptRail

import structlog

from autopr.repos.completions_repo import CompletionsRepo
from autopr.services.publish_service import PublishService

log = structlog.get_logger()

RailObjectSubclass = TypeVar('RailObjectSubclass', bound=RailObject)
BaseModelSubclass = TypeVar('BaseModelSubclass', bound=pydantic.BaseModel)


class RailService:
    """
    Service for invoking guardrails according to PromptRail and RailObject subclasses.
    See PromptRail, RailObject, and [Guardrails docs](https://docs.guardrails.io/) for more information.

    To make a guardrails call:
    - define a RailObject subclass
    - define a PromptRail subclass
    - instantiate the PromptRail
    - call `rail_service.run_prompt_rail(rail)` with the instantiated PromptRail

    For example:

        class Colors(RailObject):
            output_spec = '<list name="colors"><string/></list>'

            colors: list[str]

        class MyPromptRail(PromptRail):
            output_type = Colors
            prompt_template = "What colors is {something}?"

            something: str

        rail = MyPromptRail(something="a zebra")
        colors = rail_service.run_prompt_rail(rail)

        print(colors)  # colors=['black', 'white']

    This service is responsible for:
    - Compiling prompts according to `PromptRail.prompt_template`, `RailObject.output_spec`,
      and `RailObject.get_rail_spec()`
    - Invoking a guardrail LLM calls,
      optionally after an ordinary LLM call if `PromptRail.two_step` is True
    - Parsing the guardrail LLM response into a RailObject (pydantic) instance
    - Publishing the RailObject instance to the publish service
    - Keeping `publish_service` informed of what's going on


    Parameters
    ----------
    min_tokens: int
        Minimum number of tokens to leave in the context window to allow for response
    context_limit: int
        Context window token size limit
    num_reasks: int
        Number of times to re-ask the guardrail if it fails
    temperature: float
        Temperature to use for guardrails calls
    raw_system_prompt: str
        System prompt to use for ordinary LLM calls (if `PromptRail.two_step` is True)
    """

    def __init__(
        self,
        completions_repo: CompletionsRepo,
        publish_service: PublishService,
        min_tokens: int = 1000,
        context_limit: int = 8192,
        num_reasks: int = 2,
        temperature: float = 0.8,
        raw_system_prompt: str = 'You are a software developer and git nerd, a helpful planning and coding assistant.',
    ):
        self.completions_repo = completions_repo
        self.publish_service = publish_service
        self.min_tokens = min_tokens
        self.context_limit = context_limit
        self.num_reasks = num_reasks
        self.temperature = temperature
        self.raw_system_prompt = raw_system_prompt

    def run_rail_string(self, rail_spec: str, prompt_params: dict[str, Any]) -> Optional[dict[str, Any]]:
        """
        Run a guardrails call with the given rail spec and prompt parameters.
        """
        def completion_func(prompt: str, instructions: str):
            return self.completions_repo.complete(
                prompt=prompt,
                system_prompt=instructions,
                temperature=self.temperature,
            )

        pr_guard = gr.Guard.from_rail_string(
            rail_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )

        log.debug(
            'Running rail',
            rail_spec=rail_spec,
            prompt_params=prompt_params,
        )
        # Invoke guardrails
        raw_o, dict_o = pr_guard(
            completion_func,
            prompt_params=prompt_params
        )
        log.debug('Ran rail',
                  raw_output=raw_o,
                  dict_output=dict_o)

        if dict_o is None:
            log.warning(f'Got None from rail',
                        rail_spec=rail_spec,
                        prompt_params=prompt_params)
            return None

        return dict_o

    def run_rail_model(
        self,
        model: Type[BaseModelSubclass],
        rail_spec: str,
        prompt_params: dict[str, Any]
    ) -> Optional[BaseModelSubclass]:
        """
        Run a guardrails call with a pydantic model to parse the response into.
        """
        def completion_func(prompt: str, instructions: str):
            return self.completions_repo.complete(
                prompt=prompt,
                system_prompt=instructions,
                temperature=self.temperature,
            )

        pr_guard = gr.Guard.from_rail_string(
            rail_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )

        prompt = self.get_rail_message(rail_spec, prompt_params)
        log.debug('Running rail',
                  rail_model=model.__name__,
                  rail_message=prompt)

        # Format the prompt for publish service, such that the `<output> ... </output>` tags are put in a ```xml block
        formatted_prompt = prompt.replace('<output>', '```xml\n<output>').replace('</output>', '</output>\n```')

        # Invoke guardrails
        raw_o, dict_o = pr_guard(
            completion_func,
            prompt_params=prompt_params,
        )
        log.debug('Ran rail',
                  rail_model=model.__name__,
                  raw_output=raw_o,
                  dict_output=dict_o)

        if dict_o is None:
            self.publish_service.publish_call(
                summary=f"{model.__name__}: Guardrails rejected the output",
                prompt=formatted_prompt,
                raw_response=raw_o,
                default_open=('raw_response',)
            )
            log.warning(f'Got None from rail',
                        rail_model=model.__name__,
                        raw_output=raw_o)
            return None

        # Parse the output into a pydantic object
        try:
            parsed_obj = model.parse_obj(dict_o)
            self.publish_service.publish_call(
                summary=f"{model.__name__}: Parsed output",
                prompt=formatted_prompt,
                raw_response=raw_o,
                parsed_response=parsed_obj.json(indent=2),
                default_open=('parsed_response',)
            )
            return parsed_obj
        except pydantic.ValidationError:
            log.warning(f'Got invalid output from rail',
                        rail_object=model.__name__,
                        raw_output=raw_o,
                        dict_output=dict_o)
            self.publish_service.publish_call(
                summary=f"{model.__name__}: Failed to parse output dict",
                prompt=formatted_prompt,
                raw_response=raw_o,
                dict_response=json.dumps(dict_o, indent=2),
                error=traceback.format_exc(),
                default_open=('dict_response', 'error',)
            )

    def run_rail_object(
        self,
        rail_object: Type[RailObjectSubclass],
        raw_document: str
    ) -> Optional[RailObjectSubclass]:
        """
        Transforms the `raw_document` into a pydantic instance described by `rail_object`.
        """
        rail_spec = rail_object.get_rail_spec()
        return self.run_rail_model(
            model=rail_object,
            rail_spec=rail_spec,
            prompt_params={
                'raw_document': raw_document,
            },
        )

    def run_prompt_rail(
        self,
        rail: PromptRail
    ) -> Optional[RailObject]:
        """
        Runs a PromptRail, asking the LLM a question and parsing the response into `PromptRail.output_type`.

        :param rail:
        :return:
        """
        # Make sure the prompt is not too long
        max_length = self.context_limit - self.min_tokens
        success = rail.ensure_token_length(max_length)
        if not success:
            return None

        suffix = "two steps" if rail.two_step else "one step"
        self.publish_service.publish_update(f"Running rail {rail.__class__.__name__} in {suffix}...")

        # Run the rail
        prompt = rail.get_prompt_message()
        if rail.two_step:
            initial_prompt = prompt
            prompt = self.completions_repo.complete(
                prompt=initial_prompt,
                system_prompt=self.raw_system_prompt,
            )
            self.publish_service.publish_call(
                summary=f"Ran raw query",
                prompt=initial_prompt,
                response=prompt,
            )
        return self.run_rail_object(rail.output_type, prompt)

    @staticmethod
    def get_rail_message(
        rail_spec: str,
        prompt_params: dict[str, Any]
    ):
        pr_guard = gr.Guard.from_rail_string(rail_spec)
        return pr_guard.base_prompt.format(**prompt_params)

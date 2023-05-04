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

T = TypeVar('T', bound=RailObject)


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
    rail_system_prompt: str
        System prompt to use for rail guardrails calls
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
        rail_system_prompt: str = "You are a helpful assistant, "
                                  "able to express yourself purely through JSON, "
                                  "strictly and precisely adhering to the provided XML schemas.",
    ):
        self.completions_repo = completions_repo
        self.publish_service = publish_service
        self.min_tokens = min_tokens
        self.context_limit = context_limit
        self.num_reasks = num_reasks
        self.temperature = temperature
        self.raw_system_prompt = raw_system_prompt
        self.rail_system_prompt = rail_system_prompt

    def run_rail_object(self, rail_object: Type[T], raw_document: str) -> Optional[T]:
        """
        Transforms the `raw_document` into a pydantic instance described by `rail_object`.
        """
        def completion_func(prompt: str):
            return self.completions_repo.complete(
                prompt=prompt,
                system_prompt=self.rail_system_prompt,
                temperature=self.temperature,
            )

        rail_spec = rail_object.get_rail_spec()
        pr_guard = gr.Guard.from_rail_string(
            rail_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )

        prompt = self.get_rail_message(rail_object, raw_document)
        log.debug('Running rail',
                  rail_object=rail_object.__name__,
                  rail_message=prompt)

        # Format the prompt for publish service, such that the `<output> ... </output>` tags are put in a ```xml block
        formatted_prompt = prompt.replace('<output>', '```xml\n<output>').replace('</output>', '</output>\n```')

        # Invoke guardrails
        raw_o, dict_o = pr_guard(
            completion_func,
            prompt_params={
                'raw_document': raw_document,
            },
        )
        log.debug('Ran rail',
                  rail_object=rail_object.__name__,
                  raw_output=raw_o,
                  dict_output=dict_o)

        if dict_o is None:
            self.publish_service.publish_call(
                summary=f"{rail_object.__name__}: Guardrails rejected the output",
                prompt=formatted_prompt,
                raw_response=raw_o,
                default_open=('raw_response',)
            )
            log.warning(f'Got None from rail',
                        rail_object=rail_object.__name__,
                        raw_output=raw_o)
            return None

        # Parse the output into a pydantic object
        try:
            parsed_obj = rail_object.parse_obj(dict_o)
            self.publish_service.publish_call(
                summary=f"{rail_object.__name__}: Parsed output",
                prompt=formatted_prompt,
                raw_response=raw_o,
                parsed_response=parsed_obj.json(indent=2),
                default_open=('parsed_response',)
            )
            return parsed_obj
        except pydantic.ValidationError:
            log.warning(f'Got invalid output from rail',
                        rail_object=rail_object.__name__,
                        raw_output=raw_o,
                        dict_output=dict_o)
            self.publish_service.publish_call(
                summary=f"{rail_object.__name__}: Failed to parse output dict",
                prompt=formatted_prompt,
                raw_response=raw_o,
                dict_response=json.dumps(dict_o, indent=2),
                error=traceback.format_exc(),
                default_open=('dict_response', 'error',)
            )
        return None

    def run_prompt_rail(self, rail: PromptRail) -> Optional[RailObject]:
        """
        Runs a PromptRail, asking the LLM a question and parsing the response into `PromptRail.output_type`.

        :param rail:
        :return:
        """
        # Make sure there are at least `min_tokens` tokens left
        token_length = self.calculate_prompt_length(rail)
        while self.context_limit - token_length < self.min_tokens:
            # Trim the params (by default drops an item from a list)
            if not rail.trim_params():
                rail_name = rail.__class__.__name__
                log.debug(f'Could not trim params on rail {rail_name}: {rail.get_string_params()}')
                return None
            token_length = self.calculate_prompt_length(rail)

        suffix = "two steps" if rail.two_step else "one step"
        self.publish_service.publish_update(f"Running rail {rail.__class__.__name__} in {suffix}...")

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
    def get_rail_message(rail_object: type[RailObject], raw_document: str):
        spec = rail_object.get_rail_spec()
        pr_guard = gr.Guard.from_rail_string(spec)
        return pr_guard.base_prompt.format(raw_document=raw_document)

    def calculate_prompt_length(self, rail: PromptRail) -> int:
        prompt = rail.get_prompt_message()
        return len(self.completions_repo.tokenizer.encode(prompt))

    def calculate_rail_length(self, rail_object: Type[RailObject], raw_document: str) -> int:
        rail_message = self.get_rail_message(rail_object, raw_document)
        return len(self.completions_repo.tokenizer.encode(rail_message))

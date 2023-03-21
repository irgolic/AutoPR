from typing import Callable, Any, Optional, TypeVar
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

import openai
import pydantic
import transformers

import guardrails as gd
from autopr.models.rail_objects import RailObject
from autopr.models.rails import RailUnion

import structlog
log = structlog.get_logger()

T = TypeVar('T', bound=RailObject)


class RailService:
    def __init__(
        self,
        max_tokens: int = 2000,
        min_tokens: int = 1000,
        context_limit: int = 8192,
        completion_func: Callable = openai.ChatCompletion.create,
        completion_model: str = 'gpt-4',
        num_reasks: int = 2,
        temperature: float = 0.8,
        system_prompt: str = 'You are a python developer and git nerd, '
                             'able to express yourself purely through JSON, '
                             'strictly and precisely adhering to the provided XML schemas.',
    ):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.context_limit = context_limit
        self.completion_func = completion_func
        self.completion_model = completion_model
        self.num_reasks = num_reasks
        self.temperature = temperature
        self.system_prompt = system_prompt
        self.tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=max_tokens)

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def _run_rail(self, rail: RailUnion) -> tuple[str, dict]:
        rail_spec = rail.rail_spec
        pr_guard = gd.Guard.from_rail_string(
            rail_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )
        length = self.calculate_prompt_length(rail)
        max_tokens = min(self.max_tokens, self.context_limit - length)
        options = {
            'model': self.completion_model,
            'max_tokens': max_tokens,
            'temperature': self.temperature,
            'prompt_params': rail.get_string_params(),
            'system_prompt': self.system_prompt,
            **rail.extra_params,
        }
        raw_o, dict_o = pr_guard(self.completion_func, **options)
        return raw_o, dict_o

    def run_rail(self, rail: RailUnion) -> Optional[T]:
        # Make sure there are at least `min_tokens` tokens left
        token_length = self.calculate_prompt_length(rail)
        while self.context_limit - token_length < self.min_tokens:
            # Trim the params (by default drops an item from a list)
            if not rail.trim_params():
                rail_name = rail.__class__.__name__
                log.debug(f'Could not trim params on rail {rail_name}: {rail.get_string_params()}')
                return None
            token_length = self.calculate_prompt_length(rail)

        log.info('Running rail',
                 rail_name=rail.__class__.__name__,
                 raw_message=self.get_prompt_message(rail))
        raw_o, dict_o = self._run_rail(rail)
        log.info('Ran rail',
                 rail_name=rail.__class__.__name__,
                 raw_output=raw_o,
                 dict_output=dict_o)
        if dict_o is None:
            log.warning(f'Got None from rail',
                        rail_name=rail.__class__.__name__,
                        raw_output=raw_o)
            return None
        try:
            return rail.output_type.parse_obj(dict_o)
        except pydantic.ValidationError:
            log.warning(f'Got invalid output from rail',
                        rail_name=rail.__class__.__name__,
                        raw_output=raw_o,
                        dict_output=dict_o)
            return None

    def get_prompt_message(self, rail: RailUnion):
        spec = rail.rail_spec
        prompt_params = rail.get_string_params()
        pr_guard = gd.Guard.from_rail_string(spec)
        return pr_guard.base_prompt.format(**prompt_params)

    def calculate_prompt_length(self, rail: RailUnion) -> int:
        prompt = self.get_prompt_message(rail)
        return len(self.tokenizer.encode(prompt))

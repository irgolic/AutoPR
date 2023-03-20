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

T = TypeVar('T', bound=RailObject)


class RailService:
    def __init__(
        self,
        max_tokens: int = 2000,
        min_tokens: int = 1000,
        context_limit: int = 8192,
        completion_func: Callable = openai.ChatCompletion.create,
        completion_model: str = 'gpt-4',
        num_reasks: int = 3,
        temperature: float = 0.8,
    ):
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.context_limit = context_limit
        self.completion_func = completion_func
        self.completion_model = completion_model
        self.num_reasks = num_reasks
        self.temperature = temperature
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
                print(f'Could not trim params on rail {rail_name}: {rail.get_string_params()}')
                return None
            token_length = self.calculate_prompt_length(rail)

        raw_o, dict_o = self._run_rail(rail)
        if dict_o is None:
            print(f'Got None from rail: {raw_o}')
            return None
        try:
            return rail.output_type.parse_obj(dict_o)
# TODO remove this line
        except pydantic.ValidationError:
            print(f'Got invalid output from rail: {raw_o}, {dict_o}')
            return None

    def calculate_prompt_length(self, rail: RailUnion) -> int:
        spec = rail.rail_spec
        prompt_params = rail.get_string_params()
        pr_guard = gd.Guard.from_rail_string(spec)
        prompt = pr_guard.base_prompt.format(**prompt_params)
        return len(self.tokenizer.encode(prompt))

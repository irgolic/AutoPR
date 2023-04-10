import os
from typing import Optional

import openai
import structlog
from tenacity import retry, retry_if_exception_type, wait_random_exponential, stop_after_attempt

from autopr.utils import tokenizer


class CompletionsRepo:
    models: str

    def __init__(
        self,
        model: str,
        max_tokens: int = 2000,
        min_tokens: int = 1000,
        context_limit: int = 8192,
        temperature: float = 0.8,
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.context_limit = context_limit
        self.temperature = temperature

        self.tokenizer = tokenizer.get_tokenizer(max_tokens)
        self.log = structlog.get_logger(repo=self.__class__.__name__)

    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        examples: Optional[list[tuple[str, str]]] = None,
        temperature: float = 0.8,
    ) -> str:
        log = self.log.bind(
            model=self.model,
            prompt=prompt,
        )
        if examples is None:
            examples = []
        if system_prompt is None:
            system_prompt = "You are a helpful assistant."

        length = len(self.tokenizer.encode(prompt))
        max_tokens = min(self.max_tokens, self.context_limit - length)

        self.log.info(
            "Running completion",
        )
        result = self._complete(
            system_prompt=system_prompt,
            examples=examples,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        log.info(
            "Completed",
            result=result,
        )
        return result

    def _complete(
        self,
        system_prompt: str,
        examples: list[tuple[str, str]],
        prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        raise NotImplementedError


class OpenAIChatCompletionsRepo(CompletionsRepo):
    models = [
        'gpt-4',
        'gpt-3.5-turbo',
    ]

    def __init__(
        self,
        api_key: str = os.environ.get("OPENAI_API_KEY"),
        model: str = 'gpt-4',
        *args,
        **kwargs,
    ):
        super().__init__(*args, model=model, **kwargs)
        self.api_key = api_key

    @retry(
        retry=retry_if_exception_type(openai.error.OpenAIError),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6)
    )
    def _complete(
        self,
        prompt: str,
        system_prompt: str,
        examples: list[tuple[str, str]],
        max_tokens: int,
        temperature: float,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        for example in examples:
            messages.append({"role": "user", "content": example[0]})
            messages.append({"role": "assistant", "content": example[1]})
        messages.append({"role": "user", "content": prompt})

        openai_response = openai.ChatCompletion.create(
            api_key=self.api_key,
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        self.log.info(
            "Ran OpenAI chat completion",
            openai_response=openai_response,
        )
        return openai_response["choices"][0]["message"]["content"]


class OpenAICompletionsRepo(CompletionsRepo):
    models = [
        'text-davinci-003',
    ]

    def __init__(
        self,
        api_key: str = os.environ.get("OPENAI_API_KEY"),
        model: str = 'davinci',
        *args,
        **kwargs,
    ):
        super().__init__(*args, model=model, **kwargs)
        self.api_key = api_key

    @retry(
        retry=retry_if_exception_type(openai.error.OpenAIError),
        wait=wait_random_exponential(min=1, max=60),
        stop=stop_after_attempt(6)
    )
    def _complete(
        self,
        prompt: str,
        system_prompt: str,
        examples: list[tuple[str, str]],
        max_tokens: int,
        temperature: float,
    ) -> str:
        prompt = system_prompt
        for example in examples:
            prompt += f"\n\n{example[0]}\n{example[1]}"
        prompt += f"\n\n{prompt}"

        openai_response = openai.Completion.create(
            api_key=self.api_key,
            model=self.model,
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        self.log.info(
            "Ran OpenAI completion",
            openai_response=openai_response,
        )
        return openai_response["choices"][0]["text"]

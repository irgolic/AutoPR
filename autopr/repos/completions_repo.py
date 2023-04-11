from typing import Optional

import openai
import openai.error
import structlog
from tenacity import retry, retry_if_exception_type, wait_random_exponential, stop_after_attempt

from autopr.utils import tokenizer


class CompletionsRepo:
    models: list[str]

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

        self.tokenizer = tokenizer.get_tiktoken_tokenizer()
        self.log = structlog.get_logger(repo=self.__class__.__name__)

    def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        examples: Optional[list[tuple[str, str]]] = None,
        temperature: Optional[float] = None,
    ) -> str:
        log = self.log.bind(
            model=self.model,
            prompt=prompt,
        )
        if examples is None:
            examples = []
        if system_prompt is None:
            system_prompt = "You are a helpful assistant."
        if temperature is None:
            temperature = self.temperature

        length = len(self.tokenizer.encode(prompt))
        max_tokens = min(self.max_tokens, self.context_limit - length)

        self.log.info(
            "Running completion",
            prompt=prompt,
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
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        if openai_response is None or not isinstance(openai_response, dict):
            self.log.error(
                "OpenAI chat completion returned invalid response",
                openai_response=openai_response,
            )
            return ""
        self.log.info(
            "Ran OpenAI chat completion",
            openai_response=openai_response,
        )
        return openai_response["choices"][0]["message"]["content"]


class OpenAICompletionsRepo(CompletionsRepo):
    models = [
        'text-davinci-003',
    ]

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
            model=self.model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        self.log.info(
            "Ran OpenAI completion",
            openai_response=openai_response,
        )
        if openai_response is None or not isinstance(openai_response, dict):
            self.log.error(
                "OpenAI chat completion returned invalid response",
                openai_response=openai_response,
            )
            return ""
        return openai_response["choices"][0]["text"]


def get_completions_repo(
    model: str = "gpt-4",
    max_tokens: int = 2000,
    min_tokens: int = 1000,
    context_limit: int = 8192,
    temperature: float = 0.8,
):
    repo_implementations = CompletionsRepo.__subclasses__()
    for repo_implementation in repo_implementations:
        if model in repo_implementation.models:
            return repo_implementation(
                model=model,
                max_tokens=max_tokens,
                min_tokens=min_tokens,
                context_limit=context_limit,
                temperature=temperature,
            )
    raise ValueError(f"Model {model} not implemented")

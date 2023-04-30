import logging
from typing import Any, Union, Optional, Callable

import openai.error
import pydantic
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from autopr.services.publish_service import PublishService
from langchain.llms.base import BaseLLM

from langchain.chat_models.base import BaseChatModel

from langchain.schema import BaseOutputParser, PromptValue

from autopr.models.prompt_chains import PromptChain
from autopr.repos.completions_repo import CompletionsRepo
from langchain import PromptTemplate, OpenAI
from langchain.chat_models import ChatOpenAI as LangChainChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class ChatOpenAI(LangChainChatOpenAI):
    request_timeout = 240

    def _create_retry_decorator(self) -> Callable[[Any], Any]:
        # override langchain's retry decorator to wait up to 240 seconds instead of 10
        min_seconds = 1
        max_seconds = 240
        return retry(
            reraise=True,
            stop=stop_after_attempt(self.max_retries),
            wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
            retry=(
                retry_if_exception_type(openai.error.Timeout)
                | retry_if_exception_type(openai.error.APIError)
                | retry_if_exception_type(openai.error.APIConnectionError)
                | retry_if_exception_type(openai.error.RateLimitError)
                | retry_if_exception_type(openai.error.ServiceUnavailableError)
            ),
        )


class ChainService:
    """
    Service that handles running langchain completions according to a PromptChain subclass.

    This service is responsible for:
    - compiling the prompt according to `PromptChain.prompt_template` and `PromptChain.get_string_params()`
    - running the prompt through langchain
    - parsing the output according to `PromptChain.output_parser`
    - Keeping `publish_service` informed of what's going on
    """
    def __init__(
        self,
        completions_repo: CompletionsRepo,
        publish_service: PublishService,
    ):
        self.completions_repo = completions_repo
        self.publish_service = publish_service

        # TODO find a better way to integrate completions repo with langchain
        #   can we make a BaseLanguageModel that takes a completions repo?
        #   or should we replace completions repo with BaseLanguageModel?
        self.model: Union[BaseChatModel, BaseLLM]
        if completions_repo.model in [
            "gpt-4",
            "gpt-3.5-turbo"
        ]:
            self.model = ChatOpenAI(
                model_name=completions_repo.model,
                temperature=completions_repo.temperature,
                max_tokens=completions_repo.max_tokens,
            )  # type: ignore
        elif completions_repo.model == "text-davinci-003":
            self.model = OpenAI(
                model_name=completions_repo.model,
                temperature=completions_repo.temperature,
                max_tokens=completions_repo.max_tokens,
            )  # type: ignore
        else:
            raise ValueError(f"Unsupported model {completions_repo.model}")

        self.log = structlog.get_logger().bind(
            model=completions_repo.model,
            service="ChainService",
        )

    def _get_model_template(
        self,
        chain: PromptChain,
        parser: Optional[BaseOutputParser],
    ) -> PromptValue:
        variables = dict(chain.get_string_params())
        variable_names = list(variables.keys())
        partial_variables = {}
        if parser is not None:
            partial_variables["format_instructions"] = parser.get_format_instructions()

        if isinstance(self.model, BaseChatModel):
            template = ChatPromptTemplate(
                messages=[
                    HumanMessagePromptTemplate.from_template(chain.prompt_template)
                ],
                input_variables=variable_names,
                partial_variables=partial_variables,
            )
        else:
            template = PromptTemplate(
                template=chain.prompt_template,
                input_variables=variable_names,
                partial_variables=partial_variables,
            )
        return template.format_prompt(**variables)

    def _run_model(self, template: PromptValue) -> Any:
        if isinstance(self.model, BaseChatModel):
            return self.model(template.to_messages()).content
        else:
            return self.model(template.to_string())

    def run_chain(self, chain: PromptChain) -> Any:
        self.publish_service.publish_update(f"Running chain {chain.__class__.__name__}")
        if chain.output_parser:
            parser = chain.output_parser()
        else:
            parser = None
        prompt_value = self._get_model_template(chain, parser)
        str_prompt = prompt_value.to_string()
        self.log.info("Running chain", prompt=str_prompt)
        output = self._run_model(prompt_value)
        self.log.info("Got result", result=output)
        if parser is not None:
            raw_output = output
            output = parser.parse(raw_output)
            if output is None:
                self.publish_service.publish_call(
                    summary=f"{parser.__class__.__name__}: Failed to parse result",
                    prompt=str_prompt,
                    raw_response=raw_output,
                    default_open=('raw_response',),
                )
            else:
                if isinstance(output, pydantic.BaseModel):
                    pretty_result = output.json(indent=2)
                else:
                    pretty_result = str(output)
                self.publish_service.publish_call(
                    summary=f"{parser.__class__.__name__}: Parsed result",
                    prompt=str_prompt,
                    raw_response=raw_output,
                    result=pretty_result,
                    default_open=('result',),
                )
            self.log.info("Parsed result", result=output)
        else:
            self.publish_service.publish_call(
                summary="Received response",
                prompt=str_prompt,
                response=output,
            )
        return output

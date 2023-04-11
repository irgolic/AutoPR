from typing import Any, Union, Optional

import structlog
from langchain.llms.base import BaseLLM

from langchain.chat_models.base import BaseChatModel

from langchain.schema import BaseOutputParser, PromptValue

from autopr.models.prompt_chains import PromptChain
from autopr.repos.completions_repo import CompletionsRepo
from langchain import PromptTemplate, OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


class ChainService:
    def __init__(
        self,
        completions_repo: CompletionsRepo,
    ):
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

        self.completions_repo = completions_repo

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
        if chain.output_parser:
            parser = chain.output_parser()
        else:
            parser = None
        prompt_value = self._get_model_template(chain, parser)
        self.log.info("Running chain", prompt=prompt_value.to_string())
        output = self._run_model(prompt_value)
        self.log.info("Got result", result=output)
        if parser is not None:
            output = parser.parse(output)
            self.log.info("Parsed result", result=output)
        return output

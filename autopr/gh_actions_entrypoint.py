import os
from typing import Any
from autopr.main import main, Settings

import yaml

from autopr.log_config import configure_logging
from autopr.services.event_service import GithubEventService

configure_logging()

import structlog
log = structlog.get_logger()


class GithubActionSettings(Settings):
    class Config:
        env_prefix = 'INPUT_'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if any(config_str in field_name for config_str in
                   ['pull_request_agent_config', 'codegen_agent_config']):
                return yaml.safe_load(raw_val)
            return cls.json_loads(raw_val)  # type: ignore


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    # OPENAI_API_KEY input variable deprecation warning
    if 'INPUT_OPENAI_API_KEY' in os.environ:
        if __name__ == '__main__':
            log.warning("Specifying the OpenAI API key with github actions `with` input variables is deprecated"
                        " and will be removed in a future version. "
                        "Please use `env`, and add an `OPENAI_API_KEY` environment variable instead.")
        os.environ['OPENAI_API_KEY'] = os.environ['INPUT_OPENAI_API_KEY']

    repo_path = os.environ['GITHUB_WORKSPACE']
    settings = GithubActionSettings.parse_obj({})  # pyright workaround
    main(
        repo_path=repo_path,
        settings=settings,
    )

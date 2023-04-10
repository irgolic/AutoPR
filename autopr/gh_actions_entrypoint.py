import os
from typing import Any
from autopr.main import main, Settings

import yaml

from autopr.log_config import configure_logging

configure_logging()

import structlog
log = structlog.get_logger()


class GithubActionSettings(Settings):
    class Config:
        env_prefix = 'INPUT_'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name in ['pull_request_agent', 'codegen_agent']:
                return yaml.safe_load(raw_val)
            return cls.json_loads(raw_val)  # type: ignore


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    repo_path = os.environ['GITHUB_WORKSPACE']
    settings = GithubActionSettings.parse_obj({})  # pyright workaround
    main(
        repo_path=repo_path,
        settings=settings,
    )

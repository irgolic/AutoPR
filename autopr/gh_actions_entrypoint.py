import json
import os
from typing import Any

from autopr.main import Settings, MainService

import yaml

from autopr.log_config import configure_logging
from autopr.services.event_service import GitHubEventService
from autopr.services.publish_service import GitHubPublishService

configure_logging()

import structlog
log = structlog.get_logger()


class GitHubActionSettings(Settings):
    class Config:
        env_prefix = 'INPUT_'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name.endswith('agent_config'):
                return yaml.safe_load(raw_val)
            return cls.json_loads(raw_val)  # type: ignore


class GithubMainService(MainService):
    settings_class = GitHubActionSettings
    publish_service_class = GitHubPublishService

    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.github_token = os.environ['INPUT_GITHUB_TOKEN']
        self.repo.git.config('--global',
                             'http.https://github.com/.extraheader',
                             f"AUTHORIZATION: bearer {self.github_token}")

    def get_repo_path(self):
        return os.environ['GITHUB_WORKSPACE']

    def get_event(self):
        event_name = os.environ['GITHUB_EVENT_NAME']
        event_path = os.environ['GITHUB_EVENT_PATH']

        # Load event
        with open(event_path, 'r') as f:
            event_json = json.load(f)

        print(json.dumps(event_json, indent=2))

        # Extract event
        event_service = GitHubEventService(
            github_token=self.github_token,
        )
        return event_service.parse_event(event_name, event_json)

    def get_publish_service(self, **additional_kwargs):
        run_id = os.environ['GITHUB_RUN_ID']

        return super().get_publish_service(
            token=self.github_token,
            run_id=run_id,
            **additional_kwargs,
        )


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    main_service = GithubMainService()
    main_service.run()

import asyncio
import json
import os
from typing import Any

from autopr.main import Settings, MainService

from autopr.log_config import configure_logging
from autopr.models.events import EventUnion
from autopr.services.platform_service import GitHubPlatformService, PlatformService
from autopr.services.publish_service import GitHubPublishService

configure_logging()

from autopr.log_config import get_logger
log = get_logger(__name__)


class GitHubActionSettings(Settings):
    class Config:
        env_prefix = 'INPUT_'

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            return cls.json_loads(raw_val)  # type: ignore


class GithubMainService(MainService):
    settings_class = GitHubActionSettings
    platform_service_class = GitHubPlatformService
    publish_service_class = GitHubPublishService

    def get_repo_path(self):
        return os.environ['GITHUB_WORKSPACE']

    def get_platform_service(self, **additional_kwargs):
        github_token = os.environ['INPUT_GITHUB_TOKEN']

        return super().get_platform_service(
            token=github_token,
            **additional_kwargs,
        )

    def get_event(self, platform_service: PlatformService) -> EventUnion:
        event_name = os.environ['GITHUB_EVENT_NAME']
        event_path = os.environ['GITHUB_EVENT_PATH']

        # Load event
        with open(event_path, 'r') as f:
            event_json = json.load(f)

        print(json.dumps(event_json, indent=2))

        # Extract event
        return platform_service.parse_event(event_json, event_name)

    def get_publish_service(self, platform_service: PlatformService, **additional_kwargs):
        run_id = os.environ['GITHUB_RUN_ID']

        return super().get_publish_service(
            platform_service=platform_service,
            run_id=run_id,
            **additional_kwargs,
        )


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    main_service = GithubMainService()
    asyncio.run(main_service.run())

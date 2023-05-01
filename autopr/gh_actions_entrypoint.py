import json
import os
from typing import Any

from git.repo import Repo

from autopr.main import main, Settings

import yaml

from autopr.log_config import configure_logging
from autopr.services.commit_service import CommitService
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


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    # OPENAI_API_KEY input variable deprecation warning
    if 'INPUT_OPENAI_API_KEY' in os.environ:
        if __name__ == '__main__':
            log.warning("Specifying the OpenAI API key with github actions `with` input variables is deprecated"
                        " and will be removed in a future version. "
                        "Please use `env`, and add an `OPENAI_API_KEY` environment variable instead.")
        os.environ['OPENAI_API_KEY'] = os.environ['INPUT_OPENAI_API_KEY']

    # Get input variables
    settings = GitHubActionSettings.parse_obj({})  # pyright workaround

    # Get github vars
    github_token = os.environ['INPUT_GITHUB_TOKEN']
    repo_path = os.environ['GITHUB_WORKSPACE']
    run_id = os.environ['GITHUB_RUN_ID']
    event_name = os.environ['GITHUB_EVENT_NAME']
    event_path = os.environ['GITHUB_EVENT_PATH']

    # Load event
    with open(event_path, 'r') as f:
        event_json = json.load(f)

    # Extract event
    event_service = GitHubEventService(
        github_token=github_token,
    )
    event = event_service.parse_event(event_name, event_json)

    # Instantiate repo
    repo = Repo(repo_path)

    # Get repo owner and name from remote URL
    remote_url = repo.remotes.origin.url
    owner, repo_name = remote_url.removesuffix(".git").split('/')[-2:]

    # Format branch name
    branch_name = settings.target_branch_name_template.format(issue_number=event.issue.number)

    # Create commit service
    commit_service = CommitService(
        repo=repo,
        repo_path=repo_path,
        branch_name=branch_name,
        base_branch_name=settings.base_branch,
    )

    # Create publish service
    publish_service = GitHubPublishService(
        issue=event.issue,
        token=github_token,
        owner=owner,
        repo_name=repo_name,
        head_branch=branch_name,
        base_branch=settings.base_branch,
        run_id=run_id,
        loading_gif_url=settings.loading_gif_url,
    )

    main(
        repo_path=repo_path,
        event=event,
        commit_service=commit_service,
        publish_service=publish_service,
        settings=settings,
    )

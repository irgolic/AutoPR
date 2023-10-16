import uuid
from typing import Type

from git.repo import Repo
from pydantic import BaseSettings

from .log_config import get_logger
from .models.events import EventUnion
from .services.action_service import ActionService
from .services.commit_service import CommitService
from .services.platform_service import PlatformService
from .services.publish_service import PublishService
from .services.trigger_service import TriggerService

from .services.workflow_service import WorkflowService
from .triggers import get_all_triggers
from .workflows import get_all_workflows


class Settings(BaseSettings):
    base_branch: str = 'main'
    target_branch_name_template: str = 'autopr/{issue_number}'
    overwrite_existing: bool = False
    loading_gif_url: str = "https://media0.giphy.com/media/l3nWhI38IWDofyDrW/giphy.gif"


class MainService:
    settings_class: Type[Settings] = Settings
    platform_service_class: Type[PlatformService] = PlatformService
    publish_service_class: Type[PublishService] = PublishService

    def __init__(self):
        self.log = get_logger(service="main")

        self.config_dir = ".autopr"  # TODO: Make this configurable

        self.settings = self.settings_class.parse_obj({})  # pyright workaround
        self.repo_path = self.get_repo_path()
        self.repo = Repo(self.repo_path)

        # Get repo owner and name from remote URL
        remote_url = self.repo.remotes.origin.url
        self.owner, self.repo_name = remote_url.removesuffix(".git").split('/')[-2:]

        self.platform_service = self.get_platform_service()
        self.event = self.get_event(self.platform_service)

        self.branch_name = self.get_branch_name()
        self.base_branch_name = self.get_base_branch_name()

        self.publish_service = self.get_publish_service(self.platform_service)

        # Create commit service
        self.commit_service = CommitService(
            repo=self.repo,
            repo_path=self.repo_path,
            branch_name=self.branch_name,
            base_branch_name=self.base_branch_name,
        )
        self.commit_service.ensure_branch_exists()

        # Create action service and agent service
        action_service = ActionService(
            repo=self.repo,
            config_dir=self.config_dir,
            platform_service=self.platform_service,
            commit_service=self.commit_service,
        )
        triggers = get_all_triggers(
            config_dir=self.config_dir,
            repo_path=self.get_repo_path(),
        )
        workflows = get_all_workflows(
            config_dir=self.config_dir,
            repo_path=self.get_repo_path(),
        )
        self.workflow_service = WorkflowService(
            workflows=workflows,
            action_service=action_service,
            publish_service=self.publish_service,
        )
        self.trigger_service = TriggerService(
            triggers=triggers,
            publish_service=self.publish_service,
            workflow_service=self.workflow_service,
        )

    async def run(self):
        # Run the triggers
        return await self.trigger_service.trigger_event(self.event)

    def get_repo_path(self):
        raise NotImplementedError

    def get_event(self, platform_service: PlatformService) -> EventUnion:
        raise NotImplementedError

    def get_platform_service(self, **additional_kwargs) -> PlatformService:
        return self.platform_service_class(
            owner=self.owner,
            repo_name=self.repo_name,
            **additional_kwargs,
        )

    def get_publish_service(self, platform_service: PlatformService, **additional_kwargs) -> PublishService:
        return self.publish_service_class(
            platform_service=platform_service,
            owner=self.owner,
            repo_name=self.repo_name,
            issue=self.event.issue,
            pr_number=self.event.pull_request.number if self.event.pull_request is not None else None,
            base_branch=self.base_branch_name,
            head_branch=self.branch_name,
            loading_gif_url=self.settings.loading_gif_url,
            overwrite_existing=self.settings.overwrite_existing,
            **additional_kwargs,
        )

    def get_branch_name(self):
        if self.event.pull_request is not None:
            return self.event.pull_request.head_branch

        # make up a random branch name
        if self.event.issue is None:
            return self.settings.target_branch_name_template.format(issue_number=uuid.uuid4())

        # uniqueify over issue number
        branch_name = self.settings.target_branch_name_template.format(issue_number=self.event.issue.number)
        if not self.settings.overwrite_existing:
            remote = self.repo.remote()
            references = remote.fetch()
            i = 2
            while f'{remote.name}/{branch_name}' in [ref.name for ref in references]:
                branch_name = self.settings.target_branch_name_template.format(
                    issue_number=self.event.issue.number) + f'-{i}'
                i += 1

        return branch_name

    def get_base_branch_name(self):
        if self.event.pull_request is not None:
            return self.event.pull_request.base_branch
        return self.settings.base_branch

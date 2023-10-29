import importlib
import json
import os
import sys
import tempfile
from typing import Optional, Any, Union
from unittest.mock import patch

import pydantic

import autopr.workflows
from autopr.main import MainService
from autopr.models.artifacts import Issue, Message
from autopr.models.config.elements import ActionConfig, WorkflowDefinition, ExtraModel
from autopr.models.events import LabelEvent, Event, EventUnion
from autopr.models.executable import ExecutableId, ContextDict
from autopr.services.action_service import ActionSubclass
from autopr.services.platform_service import PlatformService, DummyPlatformService, GitHubPlatformService
from autopr.services.publish_service import DummyPublishService


class TestMainService(MainService):
    def __init__(self, *args, test_event, repo_path, **kwargs):
        self.__event = test_event
        self.__repo_path = repo_path
        super().__init__(*args, **kwargs)

    def get_repo_path(self):
        return self.__repo_path

    def get_event(self, platform_service: PlatformService) -> EventUnion:
        if self.__event is None:
            return LabelEvent(
                pull_request=None,
                issue=Issue(
                    number=1,
                    title="Test Issue",
                    author="Tester",
                    timestamp="2021-01-01T00:00:00Z",
                    messages=[
                        Message(
                            body="Test message 1",
                            author="Tester",
                        ),
                    ]
                ),
                label="write pr",
            )
        return self.__event

    def get_platform_service(self, **additional_kwargs) -> PlatformService:
        return DummyPlatformService()

    def get_publish_service(self, platform_service: PlatformService, **additional_kwargs):
        return DummyPublishService()


def create_repo(
    triggers_config: Optional[str] = None,
    workflows_config: Optional[str] = None,
    repo_resource: Optional[str] = None,
    quiet: bool = True,
):
    quiet_str = " -q" if quiet else ""
    # initialize dummy remote (bare repo)
    remote_dir = tempfile.mkdtemp()
    os.system(f"cd {remote_dir} && git init{quiet_str} --bare --initial-branch=main")

    # initialize git repo
    repo_dir = tempfile.mkdtemp()
    os.system(f"cd {repo_dir} && git init{quiet_str} --initial-branch=main")

    # copy repo resource
    if repo_resource is not None:
        real_resource_path = os.path.join(os.path.dirname(__file__), "resources", "repos", repo_resource)
        os.system(f"rsync -a --include '.*' {real_resource_path}/ {repo_dir}/")

    # create .autopr dir
    os.system(f"cd {repo_dir} && mkdir .autopr")
    # create triggers file
    if triggers_config is not None:
        with open(os.path.join(repo_dir, ".autopr", "triggers.yml"), "w") as f:
            f.write(triggers_config)
    # else:
    #     os.system(f"cd {repo_dir} && touch .autopr/triggers.yml")

    # create workflows file
    if workflows_config is not None:
        with open(os.path.join(repo_dir, ".autopr", "workflows.yml"), "w") as f:
            f.write(workflows_config)
    # else:
    #     os.system(f"cd {repo_dir} && touch .autopr/workflows.yml")

    os.system(f"cd {repo_dir} && git add .autopr")
    os.system(f"cd {repo_dir} && git commit{quiet_str} --allow-empty -m 'init'")
    os.system(f"cd {repo_dir} && git remote add origin {remote_dir}")
    os.system(f"cd {repo_dir} && git push{quiet_str} -u origin main")

    # change dir to repo
    os.chdir(repo_dir)

    return repo_dir


def create_ephemeral_main_service(
    triggers_filename: Optional[str] = None,
    workflows_filename: Optional[str] = None,
    repo_resource: Optional[str] = None,
    event: Optional[EventUnion | str] = None,
):
    # load triggers config
    if triggers_filename is not None:
        triggers_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "triggers",
            triggers_filename
        )
        with open(triggers_path, "r") as f:
            triggers_config = f.read()
    else:
        triggers_config = None

    repo_dir = create_repo(
        triggers_config=triggers_config,
        repo_resource=repo_resource,
    )

    # load any test workflow resources
    if workflows_filename is not None:
        workflows_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "workflows",
            workflows_filename
        )
        # inject test workflows into autopr.workflows
        autopr.workflows._test_workflow_paths[:] = [workflows_path]

    # load event
    if isinstance(event, str):
        event_path = os.path.join(
            os.path.dirname(__file__),
            "resources",
            "events",
            event
        )
        with open(event_path, "r") as f:
            event_json = json.load(f)
        platform_service = GitHubPlatformService(
            token="",
            repo_name="",
            owner="",
        )
        # TODO this depends on the filename of the event json, which is not ideal
        if "cron" in event:
            event_name = "schedule"
        elif "push" in event:
            event_name = "push"
        else:
            event_name = ""
        event = platform_service.parse_event(event_json, event_name)

    # because autopr.models.config.entrypoints.StrictExecutableId (which is used by TopLevelTriggerConfig),
    # is created upon module import, and it's constructed from a list of available actions and workflows,
    # we need to reload the module after create_repo injects `.autopr/workflows.yml` and runs os.chdir
    import autopr.models.config.entrypoints as entrypoints
    importlib.reload(entrypoints)
    with patch.object(
        sys.modules["autopr.triggers"],
        "TopLevelTriggerConfig",
        entrypoints.TopLevelTriggerConfig
    ):
        return TestMainService(
            test_event=event,
            repo_path=repo_dir,
        )


async def run_workflow_manually(
    workflows_filename: str,
    workflow_id: ExecutableId,
    inputs: ContextDict,
    repo_resource: Optional[str] = None,
):
    main = create_ephemeral_main_service(
        workflows_filename=workflows_filename,
        repo_resource=repo_resource,
    )

    executable = main.workflow_service.get_executable_by_id(workflow_id, inputs)
    if not isinstance(executable, WorkflowDefinition):
        raise ValueError(f"`{workflow_id}` is not a workflow")

    return await main.workflow_service.execute_by_id(
        id_=ExecutableId(workflow_id),
        context=ContextDict(inputs),
        publish_service=main.publish_service,
    )


async def run_action_manually_with_main(
    main: MainService,
    action: Union[type[ActionSubclass], ExecutableId],
    inputs: Optional[Union[dict[str, Any], pydantic.BaseModel]] = None,
) -> dict[str, Any]:
    action_service = main.workflow_service.action_service

    if isinstance(action, type):
        action_type = action
        action_id = ExecutableId(action_type.id)
    else:
        action_id = action
        action_type = action_service.find_action(action_id)
    if action_type is None:
        raise ValueError(f"`{action_id}` is not an action according to action_service")

    # Pass inputs through
    if inputs is None:
        context = ContextDict()
    elif isinstance(inputs, dict):
        context = ContextDict(inputs)
    elif isinstance(inputs, pydantic.BaseModel):
        context = ContextDict(inputs.dict(by_alias=True))
    else:
        raise ValueError(f"Inputs must be a dict or pydantic.BaseModel, got {type(inputs)}")

    action_config = main.workflow_service.get_executable_by_id(action_id, context)
    if not isinstance(action_config, ActionConfig):
        raise ValueError(f"`{action_id}` is not an action according to workflow_service")

    # Pass all outputs through as named in the action
    output_type = action_type._get_outputs_type()
    if not isinstance(None, output_type):
        action_config.outputs = ExtraModel.parse_obj({
            key: key
            for key in output_type.__fields__
        })
    return await action_service.run_action(
        action_config=action_config,
        context=context,
        publish_service=main.publish_service,
    )


async def run_action_manually(
    action: Union[type[ActionSubclass], ExecutableId],
    inputs: Optional[Union[dict[str, Any], pydantic.BaseModel]] = None,
    repo_resource: Optional[str] = None,
) -> dict[str, Any]:
    main = create_ephemeral_main_service(
        repo_resource=repo_resource,
    )
    return await run_action_manually_with_main(
        main=main,
        action=action,
        inputs=inputs,
    )

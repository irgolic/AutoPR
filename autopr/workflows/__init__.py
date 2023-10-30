import glob
import itertools
import os.path
from typing import Optional

import pydantic
import yaml

from autopr.actions.base import get_actions_dict
from autopr.log_config import get_logger
from autopr.models.config.elements import TopLevelWorkflowConfig
from autopr.models.executable import ExecutableId

logger = get_logger(__name__)


def _collect_workflows(
    filepath: str,
    existing_actions: list[ExecutableId],
    existing_workflows: Optional[TopLevelWorkflowConfig] = None,
) -> TopLevelWorkflowConfig:
    if existing_workflows is None:
        existing_workflows = TopLevelWorkflowConfig()

    try:
        with open(filepath) as f:
            contents = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Error loading workflow {filepath}: {e}")
        return existing_workflows

    if contents is None:
        return existing_workflows
    try:
        workflows = pydantic.parse_obj_as(TopLevelWorkflowConfig, contents)
    except pydantic.ValidationError:
        logger.error(f"Invalid workflow {filepath}")
        return existing_workflows
    for workflow_id in workflows:
        if workflow_id in existing_actions:
            logger.error(f"Unknown action {workflow_id} in {filepath}")
        if workflow_id in existing_workflows:
            raise ValueError(f"Duplicated workflow id {workflow_id} in {filepath}")
    existing_workflows |= workflows

    return existing_workflows


def _load_workflows_in_folder(
    folderpath: str,
    existing_actions: list[ExecutableId],
    existing_workflows: Optional[TopLevelWorkflowConfig] = None,
) -> TopLevelWorkflowConfig:
    if existing_workflows is None:
        existing_workflows = TopLevelWorkflowConfig()

    # load all yaml files in this folder and its subfolders
    for root, dirs, files in os.walk(folderpath):
        for filename in files:
            # if is yaml
            if filename.endswith(".yaml") or filename.endswith(".yml"):
                filepath = os.path.join(root, filename)
                existing_workflows = _collect_workflows(
                    filepath,
                    existing_actions=existing_actions,
                    existing_workflows=existing_workflows,
                )
            # if is folder
            elif os.path.isdir(filename):
                folderpath = os.path.join(root, filename)
                existing_workflows = _load_workflows_in_folder(
                    folderpath,
                    existing_actions=existing_actions,
                    existing_workflows=existing_workflows,
                )

    return existing_workflows


def get_all_workflows() -> TopLevelWorkflowConfig:
    # load default workflows
    default_workflows_folder = os.path.dirname(__file__)
    existing_actions = list(get_actions_dict())
    workflows = _load_workflows_in_folder(
        default_workflows_folder,
        existing_actions=existing_actions,
    )

    # load test workflows (if any)
    for path in _test_workflow_paths:
        workflows = _collect_workflows(
            path,
            existing_actions=existing_actions,
            existing_workflows=workflows,
        )

    return workflows


_test_workflow_paths = []


if __name__ == "__main__":
    print(get_all_workflows())

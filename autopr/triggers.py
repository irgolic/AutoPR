import glob
import os

import pydantic
import yaml

from autopr.models.config.entrypoints import TopLevelTriggerConfig


def get_all_triggers(
    config_dir: str = ".autopr",
    repo_path: str = ".",
):
    trigger_paths = []
    for path in [
        os.path.join(repo_path, config_dir, "triggers.yaml"),
        os.path.join(repo_path, config_dir, "triggers.yml"),
        os.path.join(repo_path, config_dir, "triggers", "*.yaml"),
        os.path.join(repo_path, config_dir, "triggers", "*.yml"),
    ]:
        trigger_paths.extend(glob.glob(path))

    triggers = []
    for path in trigger_paths:
        with open(path) as f:
            contents = yaml.safe_load(f)
        if contents is None:
            continue
        trigger_list = pydantic.parse_obj_as(TopLevelTriggerConfig, contents)
        triggers.extend(trigger_list.triggers)

    return triggers

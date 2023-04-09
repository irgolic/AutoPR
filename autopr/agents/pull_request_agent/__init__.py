from os.path import dirname, basename, isfile, join
import glob
from typing import Union, Any
from typing_extensions import TypeAlias

from .base import PullRequestAgentBase
from autopr.services.rail_service import RailService

file_modules = glob.glob(join(dirname(__file__), "*.py"))
file_basenames = [basename(f)[:-3] for f in file_modules if isfile(f) and not f.endswith('__init__.py')]
directory_module_inits = glob.glob(join(dirname(__file__), "*", "__init__.py"))
directory_modules = [dirname(f) for f in directory_module_inits]
directory_module_basenames = [basename(f) for f in directory_modules]
__all__ = file_basenames + directory_module_basenames
from . import *


PullRequestAgent: TypeAlias = Union[tuple(PullRequestAgentBase.__subclasses__())]  # type: ignore


def get_pull_request_agent(
    pull_request_agent_id: str,
    rail_service: RailService,
    extra_params: dict[str, Any]
) -> PullRequestAgent:
    for service in PullRequestAgentBase.__subclasses__():
        if service.id == pull_request_agent_id:
            return service(
                rail_service=rail_service,
                **extra_params
            )
    raise ValueError(f"Unknown planner service: {pull_request_agent_id}")

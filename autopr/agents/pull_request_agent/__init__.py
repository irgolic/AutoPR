from os.path import dirname, basename, isfile, join
import glob
from typing import Union, Any, Optional
from typing_extensions import TypeAlias

from .base import PullRequestAgentBase
from autopr.services.rail_service import RailService
from ...services.chain_service import ChainService
from ...services.publish_service import PublishService

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
    publish_service: PublishService,
    rail_service: RailService,
    chain_service: ChainService,
    extra_params: Optional[dict[str, Any]] = None,
) -> PullRequestAgent:
    if extra_params is None:
        extra_params = {}
    for service in PullRequestAgentBase.__subclasses__():
        if service.id == pull_request_agent_id:
            return service(
                publish_service=publish_service,
                rail_service=rail_service,
                chain_service=chain_service,
                **extra_params
            )
    raise ValueError(f"Unknown planner service: {pull_request_agent_id}")

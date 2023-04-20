from os.path import dirname, basename, isfile, join
import glob
from typing import Union, Any, Optional
from typing_extensions import TypeAlias

from git.repo import Repo

from .base import BrainAgentBase
from autopr.services.diff_service import DiffService
from autopr.services.rail_service import RailService
from ..codegen_agent import CodegenAgent
from ..pull_request_agent import PullRequestAgent
from ...services.chain_service import ChainService
from ...services.commit_service import CommitService
from ...services.publish_service import PublishService

file_modules = glob.glob(join(dirname(__file__), "*.py"))
file_basenames = [basename(f)[:-3] for f in file_modules if isfile(f) and not f.endswith('__init__.py')]
directory_module_inits = glob.glob(join(dirname(__file__), "*", "__init__.py"))
directory_modules = [dirname(f) for f in directory_module_inits]
directory_module_basenames = [basename(f) for f in directory_modules]
__all__ = file_basenames + directory_module_basenames
from . import *

BrainAgent: TypeAlias = Union[tuple(BrainAgentBase.__subclasses__())]  # type: ignore


def get_brain_agent(
    brain_agent_id: str,
    rail_service: RailService,
    chain_service: ChainService,
    diff_service: DiffService,
    codegen_agent: CodegenAgent,
    pull_request_agent: PullRequestAgent,
    commit_service: CommitService,
    publish_service: PublishService,
    repo: Repo,
    extra_params: Optional[dict[str, Any]] = None,
) -> BrainAgent:
    if extra_params is None:
        extra_params = {}
    for service in BrainAgentBase.__subclasses__():
        if service.id == brain_agent_id:
            return service(
                rail_service=rail_service,
                chain_service=chain_service,
                diff_service=diff_service,
                codegen_agent=codegen_agent,
                pull_request_agent=pull_request_agent,
                commit_service=commit_service,
                publish_service=publish_service,
                repo=repo,
                **extra_params
            )
    raise ValueError(f"Unknown brain service: {brain_agent_id}")

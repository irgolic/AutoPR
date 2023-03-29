from os.path import dirname, basename, isfile, join
import glob
from typing import Union, Any, Optional
from typing_extensions import TypeAlias

from git.repo import Repo

from .base import CodegenAgentBase
from autopr.services.diff_service import DiffService
from autopr.services.rail_service import RailService

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
from . import *

CodegenAgent: TypeAlias = Union[tuple(CodegenAgentBase.__subclasses__())]  # type: ignore


def get_codegen_agent(
    codegen_id: str,
    rail_service: RailService,
    diff_service: DiffService,
    repo: Repo,
    extra_params: Optional[dict[str, Any]] = None,
) -> CodegenAgent:
    if extra_params is None:
        extra_params = {}
    for service in CodegenAgentBase.__subclasses__():
        if service.id == codegen_id:
            return service(
                rail_service=rail_service,
                diff_service=diff_service,
                repo=repo,
                **extra_params
            )
    raise ValueError(f"Unknown codegen service: {codegen_id}")

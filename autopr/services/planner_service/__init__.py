from os.path import dirname, basename, isfile, join
import glob
from typing import Union, Any
from typing_extensions import TypeAlias

from .base import PlannerServiceBase
from ..rail_service import RailService

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
from . import *


PlannerService: TypeAlias = Union[tuple(PlannerServiceBase.__subclasses__())]  # type: ignore


def get_planner_service(
    planner_id: str,
    rail_service: RailService,
    extra_params: dict[str, Any]
) -> PlannerService:
    for service in PlannerServiceBase.__subclasses__():
        if service.id == planner_id:
            return service(
                rail_service=rail_service,
                **extra_params
            )
    raise ValueError(f"Unknown planner service: {planner_id}")

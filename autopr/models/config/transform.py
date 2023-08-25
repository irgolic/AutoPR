# Transforming between config and action variables
import typing
from typing import TypeVar, Generic

from autopr.models.executable import ContextDict

RealType = TypeVar("RealType")
ConfigType = TypeVar("ConfigType")
ImplementsTransformsInContext = TypeVar("ImplementsTransformsInContext")


class TransformsInto(Generic[RealType]):
    """
    In the config, some IO types will have a different representation.
    """

    @classmethod
    def transform_from_config(
        cls,
        config_var: typing.Any,
        context: ContextDict
    ) -> RealType:
        """
        Transform a config variable into the type used in the action.
        """
        raise NotImplementedError


class TransformsFrom:  # (Generic[ConfigType]):
    """
    In the config, some IO types will have a different representation.
    """

    @classmethod
    def _get_config_type(cls):  # -> type[ConfigType]:
        raise NotImplementedError

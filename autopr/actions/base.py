import inspect
import typing
from typing import ClassVar, Type, Any, Optional, TypeVar, Generic, Union

import pydantic
from git.repo import Repo

from autopr.log_config import get_logger
from autopr.models.executable import ExecutableId
from autopr.services.cache_service import CacheService
from autopr.services.commit_service import CommitService
from autopr.services.platform_service import PlatformService
from autopr.services.publish_service import PublishService


Inputs = TypeVar('Inputs', bound=Union[pydantic.BaseModel, type(None)])
Outputs = TypeVar('Outputs', bound=Union[pydantic.BaseModel, type(None)])


class ActionMeta(type):
    """
    Metaclass for actions.
    Its only responsibility is to register actions in a global registry.
    """
    actions_registry: dict[ExecutableId, type] = {}

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict[str, Any]) -> type:
        cls = super().__new__(mcs, name, bases, attrs)
        if name == "Action":
            return cls
        if not hasattr(cls, "id"):
            raise ValueError(f"Action `{cls.__name__}` does not specify `id` class variable")
        id_ = getattr(cls, "id")
        if id_ in mcs.actions_registry and not mcs.is_same_class(cls, mcs.actions_registry[id_]):
            raise ValueError(f"Action `{cls.__name__}` has duplicate ID `{id_}`")
        mcs.actions_registry[id_] = cls
        return cls

    @staticmethod
    def is_same_class(cls1, cls2):
        return (
            inspect.getfile(cls1) == inspect.getfile(cls2)
            and cls1.__qualname__ == cls2.__qualname__
        )


class Action(Generic[Inputs, Outputs], metaclass=ActionMeta):
    """
    Base class for all actions.

    Actions are the basic unit of work in the autonomous agent.
    They are responsible for performing a single task, affecting the environment in some way,
    and returning a string describing the result of the action.
    """

    #: The ID of the action, used to identify it in the AutoPR configuration. `finished` is a reserved ID. Required.
    id: ClassVar[str]

    #: The name of the action, used to describe it to the LLM upon action selection. Optional, defaults to `id`.
    name: ClassVar[Optional[str]] = None

    #: The description of the action, used to describe it to the LLM upon action selection. Optional.
    description: ClassVar[Optional[str]] = None

    async def run(self, inputs: Inputs) -> Outputs:
        """
        Run the action.

        Read the `inputs` argument to read variables from the context.
        Return outputs to write variables to the context.
        """
        raise NotImplementedError

    def __init__(
        self,
        repo: Repo,
        publish_service: PublishService,
        platform_service: PlatformService,
        cache_service: CacheService,
        commit_service: CommitService,
        **kwargs: Any,
    ) -> None:
        # Use repo for git operations
        self.repo = repo

        # Use publish service for in-progress updates
        self.publish_service = publish_service

        # Use platform service for platform-specific operations
        self.platform_service = platform_service

        # Use cache service for caching data
        self.cache_service = cache_service

        # Use commit service for committing changes
        self.commit_service = commit_service

        # Use log for more detailed debug messages
        self.log = get_logger(service="action",
                              id=self.id)

        # Define kwargs to pass configuration to actions via `action_config`
        if kwargs:
            self.log.warning("Action received unexpected kwargs that it will ignore",
                             kwargs=kwargs)

    @classmethod
    def _get_inputs_type(cls) -> type[Inputs]:
        i = typing.get_args(cls.__orig_bases__[0])[0]  # pyright: ignore
        if isinstance(i, TypeVar):
            raise ValueError(f"Action `{cls.id}` does not specify inputs type argument")
        return i

    @classmethod
    def _get_outputs_type(cls) -> type[Outputs]:
        o = typing.get_args(cls.__orig_bases__[0])[1]  # pyright: ignore
        if isinstance(o, TypeVar):
            raise ValueError(f"Action `{cls.id}` does not specify outputs type argument")
        return o


def get_actions_dict() -> dict[ExecutableId, Type[Action[Any, Any]]]:
    # initialize all Action subclass declarations in the folder
    import autopr.actions  # pyright: ignore[reportUnusedImport]

    # return all subclasses of Action as registered in the metaclass
    return ActionMeta.actions_registry

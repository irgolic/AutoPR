from typing import ClassVar, List, Type, Collection, Any, Optional

import pydantic
import structlog
from git.repo import Repo
from pydantic import Extra

from autopr.models.rail_objects import RailObject
from autopr.services.chain_service import ChainService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService


class ContextDict(dict[str, Any]):
    """
    A dictionary of context variables passed between actions.
    Overrides `__str__` to format the context in a prompt-friendly way.
    """

    def select_keys(self, keys: Collection[str]) -> "ContextDict":
        """
        Select a subset of keys from the context.
        """
        for key in keys:
            if key not in self:
                raise KeyError(f"Key {key} not found in context")
        return ContextDict({key: self[key] for key in keys})

    @staticmethod
    def key_to_heading(key: str) -> str:
        """
        Convert a context key to a heading.
        """
        return key.replace("_", " ").title()

    def as_string(
        self,
        variable_headings: Optional[dict[str, str]] = None,
        enclosure_mark: str = "+-+",
    ):
        """
        Format the context as a string.

        Parameters
        ----------

        variable_headings
            A dictionary mapping context keys to headings.
            If not provided, the keys will be used as headings.
        enclosure_mark
            The string to use to enclose each variable.
        """
        if variable_headings is None:
            variable_headings = {}
        for key in self:
            if key not in variable_headings:
                variable_headings[key] = self.key_to_heading(key)

        context_string = "Context, each variable enclosed by " + enclosure_mark + ":\n\n"
        context_string += "\n\n".join(f"""{variable_headings[key]}:
{enclosure_mark}
{str(value)}
{enclosure_mark}""" for key, value in self.items())
        return context_string

    def __str__(self):
        return self.as_string()


class Action:
    """
    Base class for all actions.

    Actions are the basic unit of work in the autonomous agent.
    They are responsible for performing a single task, affecting the environment in some way,
    and returning a string describing the result of the action.
    """

    # The ID of the action, used to identify it in the AutoPR configuration. `finished` is a reserved ID. Required.
    id: ClassVar[str]

    # The description of the action, used to describe it to the LLM upon action selection.
    description: ClassVar[str] = ""

    class Arguments(RailObject):
        """
        Arguments for the action.
        If the action takes arguments that should be queried by the LLM (e.g., filename),
        subclass and override this class in your Action subclass,
        defining the arguments as pydantic fields.

        Example:
            ```
            class Arguments(Action.Arguments):
                filepaths: list[str]

                output_spec = "<list name='filepaths'><string/></list>"
            ```
        """

        # `output_spec` describes the structure of the arguments for guardrails,
        # to be mapped into the model subclass.
        # Soon to be deprecated, as guardrails adopts pydantic Field parameters.
        output_spec: ClassVar[str] = ""

    def run(
        self,
        args: Arguments,
        context: ContextDict,
    ) -> ContextDict:
        """
        Run the action.
        The return value should be a string describing the action's result.

        Parameters
        ----------
        args : Arguments
            The arguments provided by the LLM, as per the overridden `Arguments` class.
        context : ContextDict
            The context for the action,
            containing information about e.g., the issue, the current commit, and other actions' results.

        Returns
        -------
        ContextDict
            The updated context, adding any new information to the context.
        """
        raise NotImplementedError

    def __init__(
        self,
        repo: Repo,
        rail_service: RailService,
        chain_service: ChainService,
        publish_service: PublishService,
        **kwargs,
    ):
        # Use repo for git operations
        self.repo = repo

        # Use rail and chain services to run LLM calls
        self.rail_service = rail_service
        self.chain_service = chain_service

        # Use publish service for in-progress updates
        self.publish_service = publish_service

        # Use log for more detailed debug messages
        self.log = structlog.get_logger(service="action",
                                        id=self.id)

        # Define kwargs to pass configuration to actions via `action_config`
        if kwargs:
            self.log.warning("Action received unexpected kwargs that it will ignore",
                             kwargs=kwargs)


def get_all_actions(parent=Action) -> Collection[Type[Action]]:
    # import to initialize Action subclasses
    import autopr.actions

    descendants = set()
    for subclass in parent.__subclasses__():
        descendants.add(subclass)
        # get subclasses of subclasses
        descendants.update(get_all_actions(subclass))
    return descendants

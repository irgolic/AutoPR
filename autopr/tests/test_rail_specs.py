from unittest.mock import MagicMock

import pytest
import guardrails as gr
from autopr.actions.base import Action, ContextDict, get_all_actions

from autopr.models.rail_objects import RailObject

# Make sure to import, so all rail objects initialize
import autopr.actions
from autopr.services.action_service import ActionService


@pytest.mark.parametrize(
    "rail_type",
    RailObject.__subclasses__()
)
def test_guardrails_spec_validity(rail_type):
    """Test that all guardrails specs are valid."""
    rail_spec = rail_type.get_rail_spec()
    print(rail_spec)
    gr.Guard.from_rail_string(rail_spec)


class A(Action):
    id = "a"
    description = "i am a"

    class Arguments(Action.Arguments):
        a: str
        b: str

        output_spec = "<string name='a'/><string name='b'/>"

    def run(self, arguments: Arguments, context: ContextDict) -> ContextDict:
        return context


class B(Action):
    id = "b"

    def run(self, arguments: Action.Arguments, context: ContextDict) -> ContextDict:
        return context


action_service = ActionService(
    repo=MagicMock(),
    completions_repo=MagicMock(),
    publish_service=MagicMock(),
    rail_service=MagicMock(),
    chain_service=MagicMock(),
)


all_actions = get_all_actions()
all_action_ids = [a.id for a in all_actions]


@pytest.mark.parametrize(
    "rail_spec",
    [
        action_service._write_action_selection_rail_spec(['a'], include_finished=True),
        action_service._write_action_selection_rail_spec(['b'], include_finished=False),
        action_service._write_action_selection_rail_spec(['a', 'b'], include_finished=True),
        action_service._write_action_selection_rail_spec(['a', 'b'], include_finished=False),
        action_service._write_action_args_query_rail_spec(A.Arguments),
    ]
)
def test_mock_action_service_spec_validity(rail_spec):
    """Test that all action service specs are valid."""
    print(rail_spec)
    gr.Guard.from_rail_string(rail_spec)


@pytest.mark.parametrize(
    "rail_spec",
    [
        action_service._write_action_selection_rail_spec(all_action_ids, include_finished=True),
    ] + [
        action_service._write_action_selection_rail_spec([a_id], include_finished=True)
        for a_id in all_action_ids
    ]
)
def test_real_action_service_spec_validity(rail_spec):
    print(rail_spec)
    gr.Guard.from_rail_string(rail_spec)
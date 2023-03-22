import typing

import pytest
import guardrails as gr

from autopr.models.rails import RailUnion


@pytest.mark.parametrize(
    "rail_type",
    typing.get_args(RailUnion)
)
def test_guardrails_spec_validity(rail_type):
    """Test that all guardrails specs are valid."""
    rail_spec = rail_type.get_rail_spec()
    print(rail_spec)
    gr.Guard.from_rail_string(rail_spec)

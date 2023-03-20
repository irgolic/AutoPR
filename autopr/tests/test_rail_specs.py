import typing

import pytest
import guardrails as gd

from autopr.models.rails import RailUnion


@pytest.mark.parametrize(
    "rail_type",
    typing.get_args(RailUnion)
)
def test_guardrails_spec_validity(rail_type):
    """Test that all guardrails specs are valid."""
    print(rail_type.rail_spec)
    gd.Guard.from_rail_string(rail_type.rail_spec)

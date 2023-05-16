import pytest
import guardrails as gr

from autopr.models.rail_objects import RailObject

# Make sure to import, so all rail objects initialize
import autopr.actions


@pytest.mark.parametrize(
    "rail_type",
    RailObject.__subclasses__()
)
def test_guardrails_spec_validity(rail_type):
    """Test that all guardrails specs are valid."""
    rail_spec = rail_type.get_rail_spec()
    print(rail_spec)
    gr.Guard.from_rail_string(rail_spec)

import os

from autopr.triggers import get_all_triggers


def test_parsing_autopr_folder():
    """
    Test that the autopr folder is parsed correctly.
    """
    # Set to AutoPR repo root
    config_dir_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        ".autopr",
    )
    triggers = get_all_triggers(
        config_dir=config_dir_path,
    )
    assert triggers

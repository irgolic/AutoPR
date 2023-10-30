import os

import pytest

from autopr.models.config.entrypoints import get_params
from autopr.triggers import get_all_triggers
from autopr.workflows import get_all_workflows


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


@pytest.mark.parametrize(
    "workflow_id, expected_params",
    [
        (
            "summarize_file",
            {
                "EMPTY_FILE_SUMMARY": "This file is empty.",
                "FILE_SUMMARY_INSTRUCTIONS": "Respond in 3-5 sentences.",
                "FILE_SUMMARY_PROMPT": "What is the purpose of this file? Respond in 3-5 sentences.",
            },
        ),
        (
            "summarize_folder",
            {
                "EMPTY_FILE_SUMMARY": "This file is empty.",
                "FILE_SUMMARY_INSTRUCTIONS": "Respond in 3-5 sentences.",
                "FILE_SUMMARY_PROMPT": "What is the purpose of this file? Respond in 3-5 sentences.",
                "FOLDER_SUMMARY_INSTRUCTIONS": "Respond in 3-5 sentences.",
                "FOLDER_SUMMARY_PROMPT": "What's this folder all about? Respond in 3-5 sentences.",
                "IGNORE_FILES": [],
            },
        ),
        (
            "generate_readme_summaries",
            {
                "EMPTY_FILE_SUMMARY": "This file is empty.",
                "FILE_SUMMARY_INSTRUCTIONS": "Respond in 3-5 sentences.",
                "FILE_SUMMARY_PROMPT": "What is the purpose of this file? Respond in 3-5 sentences.",
                "FOLDER_SUMMARY_INSTRUCTIONS": "Respond in 3-5 sentences.",
                "FOLDER_SUMMARY_PROMPT": "What's this folder all about? Respond in 3-5 sentences.",
                "IGNORE_FILES": [],
            },
        ),
    ],
)
def test_get_params(workflow_id, expected_params):
    all_workflows = get_all_workflows()
    param_spec = get_params(workflow_id, all_workflows)
    assert param_spec == expected_params

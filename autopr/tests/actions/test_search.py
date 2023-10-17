import os
from typing import Any, Optional

import pydantic
import pytest

from autopr.models.executable import ContextDict, ExecutableId
from autopr.tests.mock_openai import mock_openai
from autopr.tests.utils import run_action_manually

from autopr.actions.search import SearchHit


@pytest.mark.parametrize(
    "inputs, expected_output, repo_resource",
    [
        (
            {
                "query": "FILE",
            },
            {
                "hits": [
                    SearchHit(
                        filepath="rootTestFile.js",
                        line_number=6,
                        char_number=3
                    ),
                    SearchHit(
                        filepath="rootTestFile.html",
                        line_number=7,
                        char_number=3
                    ),
                    SearchHit(
                        filepath="subfolder/subfolderFile.js",
                        line_number=6,
                        char_number=3
                    ),
                    SearchHit(
                        filepath="subfolder/subfolderFile.html",
                        line_number=7,
                        char_number=5
                    ),
                ]
            },
            "repo_for_searching",
        ),
        (
            {
                "query": "FILE",
                "directory_path": "subfolder",
            },
            {
                "hits": [
                    SearchHit(
                        filepath="subfolder/subfolderFile.js",
                        line_number=6,
                        char_number=3
                    ),
                    SearchHit(
                        filepath="subfolder/subfolderFile.html",
                        line_number=7,
                        char_number=5
                    ),
                ]
            },
            "repo_for_searching",
        ),
        (
            {
                "query": "FILE",
                "entries_to_ignore": ["subfolder"],
            },
            {
                "hits": [
                    SearchHit(
                        filepath="rootTestFile.js",
                        line_number=6,
                        char_number=3
                    ),
                    SearchHit(
                        filepath="rootTestFile.html",
                        line_number=7,
                        char_number=3
                    ),
                ]
            },
            "repo_for_searching",
        ),
    ],
)
@pytest.mark.asyncio
async def test_actions(
    mocker,
    inputs: ContextDict,
    expected_output: dict[str, Any],
    repo_resource: Optional[str],
):
    outputs = await run_action_manually(
        action=ExecutableId("search"),
        inputs=ContextDict(inputs),
        repo_resource=repo_resource,
    )
    assert outputs == expected_output

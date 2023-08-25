import os

from typing import Any, Optional

import pydantic
import pytest

from autopr.actions.utils.prompt_context import PromptContext, PromptContextEntry
from autopr.models.executable import ContextDict, ExecutableId
from autopr.tests.mock_openai import mock_openai

from autopr.tests.utils import run_action_manually


@pytest.mark.parametrize(
    "inputs, expected_ls, repo_resource",
    [
        (
            {
                "folder_path": ".",
            },
            [
                "Makefile",
                ".autopr",
            ],
            "example_repo_1",
        ),
    ]
)
@pytest.mark.asyncio
async def test_actions(
    mocker,
    inputs: ContextDict,
    expected_ls: list[str],
    repo_resource: Optional[str],
):
    mocker.patch(
        "openai.ChatCompletion.acreate",
        new=mock_openai,
    )
    outputs = await run_action_manually(
        action=ExecutableId("crawl_folder"),
        inputs=ContextDict(inputs),
        repo_resource=repo_resource
    )
    assert "contents" in outputs
    assert sorted(outputs["contents"]) == sorted(expected_ls)

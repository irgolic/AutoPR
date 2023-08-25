import os

from typing import Any, Optional

import pydantic
import pytest

from autopr.actions.utils.prompt_context import PromptContext, PromptContextEntry
from autopr.models.executable import ContextDict, ExecutableId
from autopr.tests.mock_openai import mock_openai

from autopr.tests.utils import run_action_manually


@pytest.mark.parametrize(
    "action_id, inputs, expected_outputs, repo_resource",
    [
        (
            "bash",
            {
                "command": "echo Hello world!",
            },
            {
                "stdout": "Hello world!\n",
                "stderr": "",
            },
            None,
        ),
        (
            "prompt",
            {
                "prompt_context": PromptContext(
                    __root__=[PromptContextEntry(
                        value="The world is beautiful, flowers are blooming, and the birds are singing.",
                        heading="Message to be summarized",
                    )]
                ),
                "prompt": "What is this message trying to convey?",
                "instructions": "Respond in a single short sentence.",
            },
            {
                "result": "The message is trying to convey the beauty of the world and the joy of nature",
            },
            None
        ),
        (
            "insert_content_into_text",
            {
                "existing_content": "Hello",
                "delimiter": "<--->",
                "content_to_add": "INSERTED",
            },
            {
                "content": "Hello\n\n<--->INSERTED<--->",
            },
            None,
        ),
        (
            "insert_content_into_text",
            {
                "existing_content": "He<--->llo",
                "delimiter": "<--->",
                "content_to_add": "INSERTED",
            },
            {
               "content": "He<--->llo\n\n<--->INSERTED<--->",
            },
            None,
        ),
        (
            "insert_content_into_text",
            {
                "existing_content": "Hello\n\n<--->World<--->",
                "delimiter": "<--->",
                "content_to_add": "INSERTED",
            },
            {
                "content": "Hello\n\n<--->INSERTED<--->",
            },
            None,
        ),
        (
            "insert_content_into_text",
            {
                "existing_content": "Hello<--->World\n\n<--->!\n\n<--->To be replaced<--->",
                "delimiter": "<--->",
                "content_to_add": "INSERTED",
            },
            {
                "content": "Hello<--->World\n\n<--->!\n\n<--->INSERTED<--->",
            },
            None,
        ),
    ]
)
@pytest.mark.asyncio
async def test_actions(
    mocker,
    action_id: ExecutableId,
    inputs: ContextDict,
    expected_outputs: dict[str, Any],
    repo_resource: Optional[str],
):
    mocker.patch(
        "openai.ChatCompletion.acreate",
        new=mock_openai,
    )
    outputs = await run_action_manually(
        action=action_id,
        inputs=ContextDict(inputs),
        repo_resource=repo_resource
    )

    assert outputs == expected_outputs

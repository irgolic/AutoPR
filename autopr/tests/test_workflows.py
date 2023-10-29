import os

from typing import Any, Optional

import pytest

from autopr.models.config.elements import WorkflowDefinition
from autopr.models.executable import ContextDict, ExecutableId
from autopr.tests.mock_openai import mock_openai

from autopr.tests.utils import create_ephemeral_main_service


@pytest.mark.parametrize(
    "workflows_filename, workflow_id, inputs, params, expected_outputs, repo_resource",
    [
        # test simple workflow
        (
            "bash.yaml",
            "bash_workflow",
            {
                "command": "echo Hello world!",
            },
            {},
            {
                "msg": "Hello world!\n",
            },
            None,
        ),
        # test multi-step workflow
        (
            "multistep_bash.yaml",
            "bash_workflow",
            {
                "command": "echo Hello world!\n",
            },
            {},
            {
                "msg": "Hello world!\n",
            },
            None,
        ),
        # test action iteration over a variable
        (
            "bash.yaml",
            "iter_var_action",
            {
                "list_of_commands": [
                    "echo Hello world!",
                    "echo ya hi",
                ],
            },
            {},
            {
                "outputs_list": [
                    "Hello world!\n",
                    "ya hi\n",
                ],
                "concatenated_outputs": "Hello world!\nya hi\n\n",
            },
            None,
        ),
        # test action iteration over a range
        (
            "bash.yaml",
            "iter_range_action",
            {},
            {},
            {
                "outputs_list": [
                    "Hello, world!\n",
                    "Hello, world!\n",
                    "Hello, world!\n",
                ],
            },
            None,
        ),
        # test action iteration over a range getting item by index
        (
            "bash.yaml",
            "iter_range_by_index_action",
            {
                "list_of_commands": [
                    "echo Hello world!",
                    "echo ya hi",
                ],
            },
            {},
            {
                "outputs_list": [
                    "Hello world!\n",
                    "ya hi\n",
                ],
                "concatenated_outputs": "Hello world!\nya hi\n\n",
            },
            None,
        ),
        # test workflow iteration over a variable
        (
            "bash.yaml",
            "iter_var_workflow",
            {
                "list_of_commands": [
                    "echo Hello world!",
                    "echo ya hi",
                ],
            },
            {},
            {
                "outputs_list": [
                    "Hello world!\n",
                    "ya hi\n",
                ],
                "concatenated_outputs": "Hello world!\nya hi\n\n",
            },
            None,
        ),
        # test workflow iteration over a range
        (
            "bash.yaml",
            "iter_range_workflow",
            {},
            {},
            {
                "hello_list": [
                    "Hello, world!\n",
                    "Hello, world!\n",
                ],
            },
            None,
        ),
        # test prompt workflow
        (
            "prompt.yaml",
            "gen_workflow",
            {},
            {},
            {
                "msg_summary": "The message is trying to convey the beauty of the world and the joy of nature"
            },
            None,
        ),
        # test using set_vars_lambda_key
        (
            "bash.yaml",
            "set_vars_lambda_var",
            {},
            {},
            {
                "one_add_one": 2,
                "zipped_dict": {'a': 1, 'b': 2, 'c': 3}
            },
            None,
        ),
        (
            None,
            "insert_into_readme",
            {
                'filepath': "README.md",
                'tag': 'tag',
                'content': 'Insert Me',
            },
            {},
            {
                'content': '\n\n<!-- tag -->Insert Me<!-- tag -->'
            },
            "example_repo_1",
        ),
        (
            "bash.yaml",
            "invoke_action_without_args",
            {
                "command": "echo Hello world!",
            },
            {},
            {},
            None,
        ),
        (
            "bash.yaml",
            "invoke_workflow_with_args",
            {
                "list_of_commands": [
                    "echo Hello world!",
                    "echo ya hi",
                ],
            },
            {},
            {},
            None,
        ),
        (
            None,
            "publish_todos",
            {},
            {
                "LANGUAGE": "javascript",
                "TODO_KEYWORDS": ["FIXME"],
            },
            {
                "issue_number_list": [1],
            },
            "repo_with_todos",
        )
    ]
)
@pytest.mark.asyncio
async def test_workflow(
    mocker,
    workflows_filename: Optional[str],
    workflow_id: ExecutableId,
    inputs: ContextDict,
    params: Optional[dict[str, Any]],
    expected_outputs: dict[str, Any],
    repo_resource: Optional[str],
):
    mocker.patch(
        "openai.ChatCompletion.acreate",
        new=mock_openai,
    )
    main = create_ephemeral_main_service(
        workflows_filename=workflows_filename,
        repo_resource=repo_resource
    )
    executable = main.workflow_service.get_executable_by_id(workflow_id, ContextDict())
    if not isinstance(executable, WorkflowDefinition):
        raise ValueError(f"`{workflow_id}` is not a workflow")

    context = ContextDict(inputs)

    if params:
        context["__params__"] = params

    outputs = await main.workflow_service.execute_by_id(
        workflow_id,
        context,
        publish_service=main.publish_service,
    )

    assert outputs == expected_outputs

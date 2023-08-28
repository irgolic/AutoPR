import json
import os
from unittest.mock import patch, Mock

import git.repo
import pytest

from autopr.models.artifacts import PullRequest, Message
from autopr.models.events import PushEvent
from autopr.services.platform_service import GitHubPlatformService
from autopr.tests.mock_openai import mock_openai
from autopr.tests.utils import create_ephemeral_main_service


@patch('requests.get')
@pytest.mark.asyncio
async def test_autogenerate_readmes(
    mock_get,
    mocker,
):
    mocker.patch(
        "openai.ChatCompletion.acreate",
        new=mock_openai,
    )
    mock_get.return_value = Mock(status_code=200, json=lambda: {})

    with open(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "data",
            "gh_push_event.json",
        )
    ) as f:
        event_json = json.load(f)

    platform_service = GitHubPlatformService(
        token="",
        repo_name="",
        owner="",
    )
    event = platform_service.parse_event(event_json, "push")

    main = create_ephemeral_main_service(
        triggers_filename="autogenerate_readmes.yaml",
        event=event,
        repo_resource="example_repo_3",
    )

    await main.run()
    assert os.path.exists("README.md")
    assert os.path.exists(
        os.path.join(
            "example_repo_3_subfolder",
            "README.md",
        )
    )
    assert os.path.exists(
        os.path.join(
            ".autopr",
            "README.md",
        )
    )

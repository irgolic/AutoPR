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

    main = create_ephemeral_main_service(
        triggers_filename="autogenerate_readmes.yaml",
        event="gh_push_event.json",
        repo_resource="example_repo_2",
    )

    await main.run()
    assert os.path.exists("README.md")
    assert os.path.exists(
        os.path.join(
            "example_repo_2_subfolder",
            "README.md",
        )
    )
    assert os.path.exists(
        os.path.join(
            ".autopr",
            "README.md",
        )
    )

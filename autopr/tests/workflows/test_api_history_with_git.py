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


@patch("requests.get")
@pytest.mark.asyncio
async def test_autogenerate_readmes(
    mock_get,
):
    mock_content = '{"hello": "world"}'
    file_name = "test/todos.txt"

    mock_get.return_value = Mock(status_code=200, content=mock_content.encode())

    main = create_ephemeral_main_service(
        triggers_filename="api_git_history.yaml",
        event="gh_cron_event.json",
    )

    await main.run()
    assert os.path.exists(file_name)
    with open(file_name) as f:
        assert f.read() == mock_content

import json
import os
from unittest.mock import patch, Mock

import git.repo
import pytest

from autopr.models.artifacts import PullRequest, Message
from autopr.services.platform_service import GitHubPlatformService
from autopr.tests.mock_openai import mock_openai
from autopr.tests.utils import create_ephemeral_main_service


@patch('requests.get')
@pytest.mark.asyncio
async def test_summarize_pr(
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
            "gh_pr_label_event.json",
        )
    ) as f:
        event_json = json.load(f)

    platform_service = GitHubPlatformService(
        token="",
        repo_name="",
        owner="",
    )
    event = platform_service.parse_event(event_json, "pull_request_target")

    main = create_ephemeral_main_service(
        triggers_filename="summarize_pr.yaml",
        event=event,
    )

    git_sha = git.repo.Repo().head.object.hexsha
    event.pull_request.base_commit_sha = git_sha  # pyright: ignore[reportOptionalMemberAccess]

    with open("newscript.py", "w") as f:
        f.write("#TODO do stuff here")

    os.system("git add -A")
    os.system("git commit -m 'firstthing'")

    outputs = await main.run()
    assert outputs == [{'issue': None, 'pull_request': PullRequest(messages=[Message(body='', author='PireIre')], number=10, title='Add find-todos action', author='PireIre', timestamp='2023-08-18T21:20:59Z', base_branch='main', head_branch='find-todos-action', base_commit_sha=git_sha), 'pr_diff': 'diff --git a/newscript.py b/newscript.py\nnew file mode 100644\nindex 0000000..02d3dc2\n--- /dev/null\n+++ b/newscript.py\n@@ -0,0 +1 @@\n+#TODO do stuff here\n\\ No newline at end of file\n', 'summary': 'Here is a summary of the changes in the pull request for each file:\n\n📄 newscript.py:\n- Added a new file `newscript.py` with mode 100644.\n- Added a line of code `#TODO do stuff here` at line 1.\n\nPlease note that the diff was trimmed for brevity.'}]

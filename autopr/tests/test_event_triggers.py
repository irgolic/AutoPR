import json
from typing import Optional

import pytest

from autopr.models.artifacts import Issue, Message
from autopr.models.events import LabelEvent, EventUnion, PushEvent, CronEvent
from autopr.models.executable import ContextDict
from autopr.services.platform_service import GitHubPlatformService
from autopr.tests.utils import create_ephemeral_main_service

issue_label_event = LabelEvent(
    pull_request=None,
    issue=Issue(
        open=True,
        number=1,
        title="Test Issue",
        author="Tester",
        timestamp="2021-01-01T00:00:00Z",
        messages=[
            Message(
                body="Test message 1",
                author="Tester",
            ),
        ],
    ),
    label="AutoPR",
)

push_event = PushEvent(
    branch="main",
)

cron_event = CronEvent(
    cron_schedule="0 0 * * *",
)


@pytest.mark.parametrize(
    "triggers_filename, workflows_filename, event, expected_resulting_context, repo_resource",
    [
        (
            "bash.yaml",
            "bash.yaml",
            issue_label_event,
            {
                "issue": issue_label_event.issue,
                "pull_request": None,
                "msg": "Hello, world!\n",
            },
            "example_repo_1",
        ),
        (
            "multistep_bash.yaml",
            "multistep_bash.yaml",
            issue_label_event,
            {
                "issue": issue_label_event.issue,
                "pull_request": None,
                "msg": "Hello, world!\n",
            },
            "example_repo_1",
        ),
        (
            "bash.yaml",
            "bash.yaml",
            push_event,
            {
                "issue": None,
                "pull_request": None,
                "msg": "Hello, world!\n",
            },
            "example_repo_1",
        ),
        (
            "bash.yaml",
            "bash.yaml",
            cron_event,
            {
                "issue": None,
                "pull_request": None,
                "msg": "Hello, world!\n",
            },
            "example_repo_1",
        ),
    ],
)
@pytest.mark.asyncio
async def test_event_triggers(
    triggers_filename: str,
    workflows_filename: str,
    event: EventUnion,
    expected_resulting_context: ContextDict,
    repo_resource: Optional[str],
):
    main = create_ephemeral_main_service(
        triggers_filename=triggers_filename,
        workflows_filename=workflows_filename,
        repo_resource=repo_resource,
        event=event,
    )

    # It's assumed that the event only has one trigger
    triggers = main.trigger_service._get_triggers_and_contexts_for_event(event)
    assert len(triggers) == 1

    outputs = await main.run()
    assert outputs == [expected_resulting_context]

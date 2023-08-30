import json
import os
from unittest.mock import patch, Mock

import pytest
from aioresponses import aioresponses

from autopr.models.artifacts import PullRequest, Message, Issue
from autopr.models.events import EventUnion, LabelEvent
from autopr.services.platform_service import GitHubPlatformService
from autopr.services.publish_service import GitHubPublishService
from datetime import datetime

@pytest.fixture
def platform_service():
    return GitHubPlatformService(
        token='my_token',
        owner='user',
        repo_name='repo',
    )


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@patch('requests.get')
@pytest.mark.asyncio
async def test_github_platform_service(
    mock_get,
    mock_aioresponse,
    platform_service,
):
    # Mock responses for each request call
    mock_aioresponse.get(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/pulls?base=branch2&head=user%253Abranch1&state=open',
        payload=[{
            'number': 1,
            'node_id': 'node1',
            "body": "123",
            "user": {
                "login": "user1"
            },
        }],
        status=200
    )

    timestamp = "2023-08-20T10:25:48Z"
    comments_url = f"https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues/1/comments"

    mock_aioresponse.get(
        f"https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues?state=open&since={timestamp}",
        payload=[{
            'number': 1,
            'node_id': 'node1',
            "title": "Ups an issue occurred.",
            "body": "I am an issue. Resolve me.",
            "user": {
                "login": "user1"
            },
            "created_at": "2023-08-19T17:38:34Z",
            "updated_at": "2023-08-20T10:25:48Z",
            "comments": 0,
            "comments_url": comments_url,
        }],
        status=200
    )

    mock_get.return_value = Mock(status_code=200, json=lambda: [])

    mock_aioresponse.post(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/pulls',
        payload={'number': 2},
        status=201
    )

    mock_aioresponse.post(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues/2/comments',
        payload={'id': 'comment1'},
        status=201
    )

    mock_aioresponse.post(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues/1/comments',
        payload={'id': 'comment1'},
        status=201
    )

    mock_aioresponse.patch(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/pulls/1',
        payload={},
        status=200
    )

    mock_aioresponse.patch(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues/comments/comment1',
        payload={},
        status=200
    )

    head_branch = 'branch1'
    base_branch = 'branch2'

    # Test _find_existing_pr
    pr_number = await platform_service.find_existing_pr(head_branch, base_branch)
    assert pr_number == 1

    # Test _create_pr
    pr_number, comment_ids = await platform_service.create_pr('title', ['body1', 'body2'], True, head_branch, base_branch)
    assert pr_number == 2
    assert comment_ids == [platform_service.PRBodySentinel, 'comment1']

    # Test _update_pr_body
    await platform_service.update_pr_body(1, 'new body')

    # Test _update_pr_comment
    await platform_service.update_comment('comment1', 'new comment')

    # Test _publish_comment
    comment_id = await platform_service.publish_comment('new comment', 1)
    assert comment_id == 'comment1'

    # Test _get_issues
    since = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    issues = await platform_service.get_issues(state="open", since=since)
    assert issues == [
        Issue(
            number=1,
            title='Ups an issue occurred.',
            author='user1',
            timestamp='2023-08-20T10:25:48Z',
            messages=[
                Message(
                    body='I am an issue. Resolve me.',
                    author='user1',
                )
            ]
        )
    ]


@pytest.mark.parametrize(
    'event_json_path, expected_event',
    [
        (
            os.path.join(
                os.path.dirname(__file__),
                'data',
                'gh_pr_label_event.json',
            ),
            LabelEvent(
                issue=None,
                pull_request=PullRequest(
                    number=10,
                    title="Add find-todos action",
                    author="PireIre",
                    timestamp="2023-08-18T21:20:59Z",
                    messages=[
                        Message(
                            author="PireIre",
                            body="",
                        ),
                        Message(
                            author="user1",
                            body="123",
                        ),
                    ],
                    head_branch="find-todos-action",
                    base_branch="main",
                    base_commit_sha="44ff01d565aa6173be802c6ef25514cd9eecc5b0",
                ),
                label="summarize",
            ),
        ),
        (
            os.path.join(
                os.path.dirname(__file__),
                'data',
                'gh_pr_label_event_2.json',
            ),
            # Actual   :LabelEvent(event_type='label', pull_request=PullRequest(messages=[Message(body='', author='irgolic'), Message(body='123', author='user1')], number=5, title='Fixup docs', author='irgolic', timestamp='2023-08-19T17:38:34Z', base_branch='main', head_bra ...
            LabelEvent(
                issue=None,
                pull_request=PullRequest(
                    number=5,
                    title="Fixup docs",
                    author="irgolic",
                    timestamp="2023-08-19T17:38:34Z",
                    messages=[
                        Message(
                            author="irgolic",
                            body="",
                        ),
                        Message(
                            author="user1",
                            body="123",
                        ),
                    ],
                    head_branch="docs",
                    base_branch="main",
                    base_commit_sha="9eba5fee62e51e1a47b8fae9d9693866d15e5c78",
                ),
                label="summarize",
            ),
        )
    ],
)
@patch('requests.get')
def test_parse_event(
    mock_get,
    platform_service,
    event_json_path: str,
    expected_event: EventUnion,
):
    mock_get.return_value = Mock(status_code=200, json=lambda: [{
        "body": "123",
        "user": {
            "login": "user1"
        },
    }])

    abs_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        event_json_path,
    )
    with open(abs_path) as f:
        event_json = json.load(f)

    event = platform_service.parse_event(event_json, 'pull_request_target')
    assert event == expected_event

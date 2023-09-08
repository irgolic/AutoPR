import json
import os
from unittest.mock import patch, Mock

import pytest
from aioresponses import aioresponses

from autopr.models.artifacts import Issue, PullRequest, Message
from autopr.models.events import EventUnion, LabelEvent
from autopr.services.platform_service import GitHubPlatformService
from autopr.services.publish_service import GitHubPublishService
from datetime import datetime
import requests_mock

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


@pytest.mark.asyncio
async def test_create_issue(mock_aioresponse, platform_service):
    mock_aioresponse.post(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues',
        payload={'number': 1},
        status=201
    )

    issue_number = await platform_service.create_issue('test_title', 'test_body')
    assert issue_number == 1


@pytest.mark.asyncio
async def test_update_issue_body(mock_aioresponse, platform_service):
    issue_number = 1
    mock_aioresponse.patch(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues/{issue_number}',
        payload={},
        status=200
    )

    await platform_service.update_issue_body(issue_number, 'new_body')


@pytest.mark.asyncio
async def test_get_issue_by_title(mock_aioresponse, platform_service):
    # Mock the response for getting issues
    issues_payload = [{
        'number': 1,
        'title': 'test_title',
        'body': 'test_body',
        'user': {'login': 'user1'},
        'updated_at': '2023-08-18T21:20:59Z',
        'comments_url': 'https://api.github.com/repos/user/repo/issues/1/comments'
    }]
    
    # Mock the response for getting issue by title
    mock_aioresponse.get(
        f'https://api.github.com/repos/{platform_service.owner}/{platform_service.repo_name}/issues',
        payload=issues_payload,
        status=200
    )

    expected_issue = Issue(
            messages=[
                Message(body='test_body', author='user1')
                ], 
            number=1, 
            title='test_title', 
            author='user1', 
            timestamp='2023-08-18T21:20:59Z'
        )
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: [])
        
        issue = await platform_service.get_issue_by_title('test_title')
        assert issue == expected_issue

@pytest.mark.parametrize(
    "file_path, branch, start_line, end_line, margin, expected_url",
    [
        # Case 1: Both start_line and end_line are not None.
        (
            "file1",
            "branch1",
            1,
            2,
            0,
            'https://github.com/user/repo/blob/123abcd/file1#L1-L2'
        ),
        # Case 2: Only start_line is not None, and end_line is None.
        (
            "file2",
            "branch2",
            3,
            None,
            0,
            'https://github.com/user/repo/blob/123abcd/file2#L3-L3'
        ),
        # Case 3: Only end_line is not None, and start_line is None.
        (
            "file3",
            "branch3",
            None,
            4,
            0,
            'https://github.com/user/repo/blob/123abcd/file3#L4-L4'
        ),
        # Case 4: Both start_line and end_line are None.
        (
            "file4",
            "branch4",
            None,
            None,
            0,
            'https://github.com/user/repo/blob/123abcd/file4'
        ),
        # Additional cases with margin
        (
            "file5",
            "branch1",
            1,
            2,
            1,
            'https://github.com/user/repo/blob/123abcd/file5#L1-L3'
        ),
        (
            "file6",
            "branch2",
            3,
            None,
            2,
            'https://github.com/user/repo/blob/123abcd/file6#L1-L5'
        ),
        (
            "file7",
            "branch3",
            None,
            4,
            3,
            'https://github.com/user/repo/blob/123abcd/file7#L1-L7'
        ),
        # In case there's space in the file path
        (
            "path/to/file 8",
            "branch4",
            None,
            1,
            1,
            'https://github.com/user/repo/blob/123abcd/path/to/file%208#L1-L2'
        )
    ]
)
@pytest.mark.asyncio
async def test_get_file_url(mocker, file_path, branch, start_line, end_line, margin, expected_url, platform_service):
    with patch.object(GitHubPlatformService, 'get_latest_commit_hash', return_value='123abcd'):
        url = await platform_service.get_file_url(file_path, branch, start_line, end_line, margin)
    assert url == expected_url

@pytest.mark.parametrize(
    "owner, repo, branch, expected_url",
    [
        ("owner1", "repo1", "branch1", "https://api.github.com/repos/owner1/repo1/git/ref/heads/branch1"),
        # Add other combinations if needed
    ]
)
def test_get_latest_commit_hash_url_construction(owner, repo, branch, expected_url, platform_service):
    with requests_mock.Mocker() as m:
        m.get(expected_url, json={'object': {'sha': '12345abcdef'}})
        platform_service.get_latest_commit_hash(owner, repo, branch)
        assert m.last_request.url == expected_url


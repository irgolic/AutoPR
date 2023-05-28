from unittest.mock import patch, Mock

from autopr.services.publish_service import GitHubPublishService


@patch('requests.get')
@patch('requests.post')
@patch('requests.patch')
def test_github_publish_service(mock_patch, mock_post, mock_get):
    # Mock responses for each request call
    mock_get.return_value = Mock(status_code=200, json=lambda: [{'number': 1, 'node_id': 'node1'}])
    mock_post.return_value = Mock(status_code=201, json=lambda: {'number': 2, 'id': 'comment1'})
    mock_patch.return_value = Mock(status_code=200, json=lambda: {})

    service = GitHubPublishService(
        token='my_token',
        run_id='123',
        owner='user',
        repo_name='repo',
        head_branch='branch1',
        base_branch='branch2',
        issue=None,
        pull_request_number=None,
        loading_gif_url="https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        overwrite_existing=False,
    )

    # Test _find_existing_pr
    pr = service._find_existing_pr()
    assert pr['number'] == 1
    assert pr['node_id'] == 'node1'

    # Test _create_pr
    pr = service._create_pr('title', ['body1', 'body2'], True)
    assert pr['number'] == 2
    assert service._comment_ids == [service.PRBodySentinel, 'comment1']

    # Test _update_pr_body
    service._update_pr_body(1, 'new body')
    mock_patch.assert_called_with(
        'https://api.github.com/repos/user/repo/pulls/1',
        headers=service._get_headers(),
        json={'body': 'new body'}
    )

    # Test _update_pr_comment
    service._update_pr_comment('comment1', 'new comment')
    mock_patch.assert_called_with(
        'https://api.github.com/repos/user/repo/issues/comments/comment1',
        headers=service._get_headers(),
        json={'body': 'new comment'}
    )

    # Test _publish_comment
    comment_id = service._publish_comment('new comment', 1)
    assert comment_id == 'comment1'

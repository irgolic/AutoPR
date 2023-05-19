from typing import Any

import requests
import structlog

from autopr.models.artifacts import Issue, Message, PullRequest
from autopr.models.events import IssueLabelEvent, EventUnion, PullRequestCommentEvent


class EventService:
    """
    Service for parsing events that trigger AutoPR into one of the `EventUnion` types.

    To support other platforms (Gitlab/Bitbucket/Gitea), subclass this and override `parse_event`.
    See irgolic/AutoPR#46 for more details.
    """

    def parse_event(self, event_name: str, event: dict[str, Any]) -> EventUnion:
        raise NotImplementedError


class GitHubEventService(EventService):
    """
    Service for parsing GitHub events into one of the `EventUnion` types.

    Currently only supports `IssueLabelEvent`, which is triggered when a label is added to an issue.

    See https://docs.github.com/en/webhooks-and-events/events/issue-event-types
    """

    def __init__(
        self,
        github_token: str,
    ):
        self.github_token = github_token
        self.log = structlog.get_logger()

    def get_headers(self):
        return {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {self.github_token}'
        }

    def _to_issue_label_event(self, event: dict[str, Any]) -> IssueLabelEvent:
        """
        See https://docs.github.com/en/webhooks-and-events/events/issue-event-types#labeled
        """
        # Get issue comments
        url = event['issue']['comments_url']
        assert url.startswith('https://api.github.com/repos/'), "Unexpected comments_url"
        self.log.info("Getting issue comments", url=url)
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comments_json = response.json()
        self.log.info("Got issue comments", comments=comments_json)

        # Get body
        comments_list = []
        body_message = Message(
            body=event['issue']['body'] or "",
            author=event['issue']['user']['login'],
        )
        comments_list.append(body_message)

        # Get comments
        for comment_json in comments_json:
            comment = Message(
                body=comment_json['body'] or "",
                author=comment_json['user']['login'],
            )
            comments_list.append(comment)

        # Create issue
        issue = Issue(
            number=event['issue']['number'],
            title=event['issue']['title'],
            author=event['issue']['user']['login'],
            messages=comments_list,
        )

        return IssueLabelEvent(
            issue=issue,
            label=event['label']['name'],
        )

    def _to_pull_request_comment_event(self, event: dict[str, Any]) -> PullRequestCommentEvent:
        """
        See https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#issue_comment
        """
        headers = self.get_headers()

        # Get issue comments
        url = event['issue']['comments_url']
        assert url.startswith('https://api.github.com/repos/'), "Unexpected comments_url"
        self.log.info("Getting issue comments", url=url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comments_json = response.json()
        self.log.info("Got issue comments", comments=comments_json)

        # Get body
        comments_list = []
        body_message = Message(
            body=event['issue']['body'] or "",
            author=event['issue']['user']['login'],
        )
        comments_list.append(body_message)

        # Get comments
        for comment_json in comments_json:
            comment = Message(
                body=comment_json['body'] or "",
                author=comment_json['user']['login'],
            )
            comments_list.append(comment)

        # Get pull request
        url = event['issue']['pull_request']['url']
        assert url.startswith('https://api.github.com/repos/'), "Unexpected pull_request url"
        self.log.info("Getting pull request", url=url)
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        pull_request_json = response.json()
        self.log.info("Got pull request", pull_request=pull_request_json)

        # Get branch names
        head_branch = pull_request_json['head']['ref']
        base_branch = pull_request_json['base']['ref']

        # Create pull request
        pull_request = PullRequest(
            number=event['issue']['number'],
            title=event['issue']['title'],
            author=event['issue']['user']['login'],
            messages=comments_list,
            head_branch=head_branch,
            base_branch=base_branch,
        )

        return PullRequestCommentEvent(
            pull_request=pull_request,
            new_comment=Message(
                body=event['comment']['body'] or "",
                author=event['comment']['user']['login'],
            ),
        )


    def parse_event(self, event_name: str, event_dict: dict[str, Any]):
        if event_name == 'issues':
            return self._to_issue_label_event(event_dict)
        elif event_name == 'issue_comment':
            return self._to_pull_request_comment_event(event_dict)
        raise ValueError(f"Unsupported event name: {event_name}")

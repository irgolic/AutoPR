from typing import Any

import requests
import structlog

from autopr.models.artifacts import Issue, Message
from autopr.models.events import IssueLabeledEvent, EventUnion


class EventService:
    def parse_event(self, event_name: str, event: dict[str, Any]) -> EventUnion:
        raise NotImplementedError


class GithubEventService(EventService):
    def __init__(
        self,
        github_token: str,
    ):
        self.github_token = github_token
        self.log = structlog.get_logger()

    def _to_issue_labeled_event(self, event: dict[str, Any]) -> IssueLabeledEvent:
        # Get issue comments
        url = event['issue']['comments_url']
        assert url.startswith('https://api.github.com/repos/'), "Unexpected comments_url"
        self.log.info("Getting issue comments", url=url)
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'Bearer {self.github_token}'
        }
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
        comments = {}
        for comment_json in comments_json:
            comment_id = comment_json['id']
            comment = Message(
                body=comment_json['body'] or "",
                author=comment_json['user']['login'],
            )
            comments[comment_id] = comment
            comments_list.append(comment)

        # Create issue
        issue = Issue(
            number=event['issue']['number'],
            title=event['issue']['title'],
            author=event['issue']['user']['login'],
            messages=comments_list,
        )

        return IssueLabeledEvent(
            issue=issue,
            label=event['label']['name'],
        )

    def parse_event(self, event_name: str, event_dict: dict[str, Any]):
        if event_name == 'issues':
            return self._to_issue_labeled_event(event_dict)
        raise ValueError(f"Unsupported event name: {event_name}")

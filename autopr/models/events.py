from typing import Literal, Union

import pydantic

from autopr.models.artifacts import Issue, Message, PullRequest  # , CodeComment


class Event(pydantic.BaseModel):
    """
    Events trigger AutoPR to run in different ways.
    """
    event_type: str


class IssueLabelEvent(Event):
    """
    Event triggered when a label is added to an issue.
    """
    event_type: Literal['issue_label'] = 'issue_label'

    issue: Issue
    label: str


class PullRequestCommentEvent(Event):
    """
    Event triggered when a comment is added to a pull request.
    """
    event_type: Literal['pull_request_comment'] = 'pull_request_comment'

    pull_request: PullRequest
    new_comment: Message


# class CodeReviewEvent(Event):
#     """
#     Event triggered when a comment is added to a code review.
#     """
#     event_type: Literal['code_review'] = 'code_review'
#
#     pull_request: PullRequest
#     new_code_comments: list[CodeComment]
#     new_comment: Message


EventUnion = Union[IssueLabelEvent, PullRequestCommentEvent]  # | CodeReviewEventa

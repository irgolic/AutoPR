from typing import Literal, Union, Optional

import pydantic

from autopr.models.artifacts import Issue, Message, PullRequest  # , CodeComment


class Event(pydantic.BaseModel):
    """
    Events trigger AutoPR to run in different ways.
    """
    event_type: str

    pull_request: Optional[PullRequest] = None
    issue: Optional[Issue] = None


class LabelEvent(Event):
    """
    Event triggered when a label is added to an issue or pull request.
    """
    event_type: Literal['label'] = 'label'

    label: str


class CommentEvent(Event):
    """
    Event triggered when a comment is added to an issue or pull request.
    """
    event_type: Literal['comment'] = 'comment'

    comment: Message


class PushEvent(Event):
    """
    Event triggered when a push is made to a branch.
    """
    event_type: Literal['push'] = 'push'

    branch: str


# class CodeReviewEvent(Event):
#     """
#     Event triggered when a comment is added to a code review.
#     """
#     event_type: Literal['code_review'] = 'code_review'
#
#     pull_request: PullRequest
#     new_code_comments: list[CodeComment]
#     new_comment: Message


EventUnion = Union[LabelEvent, CommentEvent, PushEvent]  # | CodeReviewEvent

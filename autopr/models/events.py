from typing import Literal, Union

import pydantic

from autopr.models.artifacts import Issue, Message


class Event(pydantic.BaseModel):
    event_type: str


class IssueOpenedEvent(Event):
    event_type: Literal['issue_opened'] = 'issue_opened'

    issue: Issue


class IssueCommentEvent(Event):
    event_type: Literal['issue_closed'] = 'issue_closed'

    issue: Issue
    new_comment: Message


EventUnion = Union[tuple(Event.__subclasses__())]  # type: ignore

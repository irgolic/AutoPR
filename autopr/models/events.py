from typing import Literal, Union

import pydantic

from autopr.models.artifacts import Issue, Message


class Event(pydantic.BaseModel):
    event_type: str


class IssueLabeledEvent(Event):
    event_type: Literal['issue_opened'] = 'issue_opened'

    issue: Issue
    label: str


# TODO implement more event types (i.e., code review)

EventUnion = IssueLabeledEvent

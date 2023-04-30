from typing import Literal, Union

import pydantic

from autopr.models.artifacts import Issue, Message


class Event(pydantic.BaseModel):
    """
    Events trigger AutoPR to run in different ways.

    TODO implement more event types (i.e., code review)
    """
    event_type: str


class IssueLabeledEvent(Event):
    """
    Event triggered when a label is added to an issue.
    """
    event_type: Literal['issue_opened'] = 'issue_opened'

    issue: Issue
    label: str


EventUnion = IssueLabeledEvent

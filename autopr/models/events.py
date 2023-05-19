from typing import Literal, Union

import pydantic

from autopr.models.artifacts import Issue, Message


class Event(pydantic.BaseModel):
    """
    Events trigger AutoPR to run in different ways.

    TODO implement more event types (i.e., code review)
    """
    event_type: str


class IssueLabelEvent(Event):
    """
    Event triggered when a label is added to an issue.
    """
    event_type: Literal['issue_label'] = 'issue_label'

    issue: Issue
    label: str


EventUnion = IssueLabelEvent

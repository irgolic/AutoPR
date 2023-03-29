from typing import Literal

import pydantic

from autopr.models.artifacts import Issue


class Event(pydantic.BaseModel):
    event_type: str


class IssueOpenedEvent(Event):
    event_type: Literal['issue_opened']

    issue: Issue


EventUnion = Union[tuple(Event.__subclasses__())]  # type: ignore

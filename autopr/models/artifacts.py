import typing

import pydantic
from typing_extensions import TypeAlias


class Issue(pydantic.BaseModel):
    number: int
    title: str
    body: str

    def to_str(self):
        return f"#{self.number} {self.title}\n\n{self.body}\n\n"


DiffStr: TypeAlias = str

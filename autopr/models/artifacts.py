import typing

import pydantic


class Issue(pydantic.BaseModel):
    number: int
    title: str
    body: str

    def to_str(self):
        return f"#{self.number} {self.title}\n\n{self.body}\n\n"


DiffStr = typing.NewType("DiffStr", str)

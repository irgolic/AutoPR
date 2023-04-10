import typing

import pydantic
from typing_extensions import TypeAlias


class Message(pydantic.BaseModel):
    body: str
    author: str

    def __str__(self):
        return f"{self.author}: {self.body}\n\n"


class Thread(pydantic.BaseModel):
    messages: list[Message]

    def __str__(self):
        return "\n".join(str(message) for message in self.messages)


class Issue(Thread):
    number: int
    title: str
    author: str

    def __str__(self):
        return f"#{self.number} {self.title}\n\n" + super().__str__()


DiffStr: TypeAlias = str

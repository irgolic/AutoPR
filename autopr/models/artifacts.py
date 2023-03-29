import typing

import pydantic
from typing_extensions import TypeAlias


class Message(pydantic.BaseModel):
    body: str
    author: str

    def to_str(self):
        return f"{self.author}: {self.body}\n\n"


class Thread(pydantic.BaseModel):
    messages: list[Message]

    def to_str(self):
        return "\n".join(message.to_str() for message in self.messages)


class Issue(Thread):
    number: int
    title: str
    author: str

    def to_str(self):
        return f"#{self.number} {self.title}\n\n" + "\n".join(
            message.to_str() for message in self.messages
        )


DiffStr: TypeAlias = str

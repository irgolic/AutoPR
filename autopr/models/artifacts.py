from typing import Literal, Optional

import pydantic
from typing_extensions import TypeAlias


class Message(pydantic.BaseModel):
    body: str = ""
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


class PullRequest(Issue):
    base_branch: str
    head_branch: str
    # code_review: list[CodeComment]

    def __str__(self):
        return f"#{self.number} {self.title}\n\n" + "\n".join(
            str(message) for message in self.messages
        )
        # ) + "\n\n" + "\n".join(
        #     str(thread) for thread in self.code_review
        # )


# class CodeComment(Thread):
#     commit_sha: str
#     filepath: str
#     status: Literal["APPROVE", "REQUEST_CHANGES", "COMMENT"]
#
#     start_line_number: int
#     end_line_number: Optional[int] = None
#
#     def __str__(self):
#         return f"{self.commit_sha}\n" \
#                f"{self.filepath}:L{self.start_line_number}" + f"{f'-L{self.end_line_number}' if self.end_line_number else ''}\n" \
#                f"{self.status}\n\n" + "\n".join(str(message) for message in self.messages)


DiffStr: TypeAlias = str

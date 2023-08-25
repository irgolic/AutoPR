from typing import Optional

from pydantic import BaseModel

from autopr.actions.base import Action


class Inputs(BaseModel):
    comment: str
    issue_number: Optional[int] = None


class Comment(Action[Inputs, None]):
    """
    A class representing an action to publish a comment on a GitHub issue.
    """
    id = "comment"

    async def run(self, inputs: Inputs) -> None:
        await self.publish_service.publish_comment(inputs.comment, inputs.issue_number)

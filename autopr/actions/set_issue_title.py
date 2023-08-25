from pydantic import BaseModel

from autopr.actions.base import Action


class Inputs(BaseModel):
    title: str


class SetIssueTitle(Action[Inputs, None]):
    """
    A class representing an action to set the title of an issue.
    """
    id = "set_issue_title"

    async def run(self, inputs: Inputs) -> None:
        await self.publish_service.set_title(inputs.title)

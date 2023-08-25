from typing import Optional

import pydantic

from autopr.actions.base import Action


class Inputs(pydantic.BaseModel):
    commit_message: str = "AutoPR commit"
    filepaths: Optional[list[str]] = None


class CommitAndPush(Action[Inputs, None]):
    """
    A class that represents an action to commit and push changes to a remote repository.
    """

    id = "commit_and_push"

    async def run(self, inputs: Inputs) -> None:
        self.commit_service.commit(
            commit_message=inputs.commit_message,
            filepaths=inputs.filepaths,
            push=True,
        )

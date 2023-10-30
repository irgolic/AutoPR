import asyncio
import re
from typing import Optional
from autopr.actions.base import Action
from pydantic import BaseModel
import os
from unittest.mock import patch
from autopr.services.platform_service import PlatformService

from autopr.models.artifacts import Issue


class Inputs(BaseModel):
    # Title of the issue
    issue_title: str

    # Body of the issue
    issue_body: str

    # Labels to add to the issue
    issue_labels: Optional[list[str]] = None

    # Whether to update an issue if it already exists
    issue_number: Optional[int] = None


class Outputs(BaseModel):
    # The issue number of the published/updated issue.
    issue_number: Optional[int]


class PublishIssue(Action[Inputs, Outputs]):
    """
    Publishes issue with the specified title if it doesn't exist yet.
    """

    id = "publish_issue"

    async def run(self, inputs: Inputs) -> Outputs:
        if inputs.issue_number is None:
            issue_number = await self.platform_service.create_issue(
                inputs.issue_title, inputs.issue_body, inputs.issue_labels
            )
            return Outputs(issue_number=issue_number)
        await self.platform_service.update_issue_body(
            inputs.issue_number, inputs.issue_body, inputs.issue_labels
        )
        return Outputs(issue_number=inputs.issue_number)


if __name__ == "__main__":
    # IMPORTANT: Here, method publish_issue is mocked and does not actually publish an issue to a repository.
    from autopr.tests.utils import run_action_manually

    with patch.object(PlatformService, "publish_issue") as mock:
        asyncio.run(
            # Run the action manually
            run_action_manually(
                action=PublishIssue,
                inputs=Inputs(
                    issue_title="Test Issue",
                    issue_body="This is a test issue",
                ),
            )
        )

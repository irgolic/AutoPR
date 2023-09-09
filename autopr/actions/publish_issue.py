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

    # Whether to update the issue if it already exists
    update_if_exists: bool = True


class Outputs(BaseModel):
    # The issue number of the published/updated issue.
    issue_number: Optional[int]


class PublishIssue(Action[Inputs, Outputs]):
    """
    Publishes issue with the specified title if it doesn't exist yet.
    """
    id = "publish_issue"

    async def run(self, inputs: Inputs) -> Outputs:
        issue = await self.platform_service.get_issue_by_title(inputs.issue_title)
        if issue is None:
            issue_number = await self.platform_service.create_issue(inputs.issue_title, inputs.issue_body)
            return Outputs(issue_number=issue_number)
        elif issue is not None and inputs.update_if_exists:
            await self.platform_service.update_issue_body(issue.number, inputs.issue_body)
            return Outputs(issue_number=issue.number)
        return Outputs(issue_number=None)

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
                    update_if_exists=True,
                ),
            )
        )

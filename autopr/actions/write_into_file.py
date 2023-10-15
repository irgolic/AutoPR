import asyncio
import os
from typing import Any, Optional

from pydantic import BaseModel

from autopr.actions.base import Action


class Inputs(BaseModel):
    # The path of the file you want to write into.
    filepath: str

    # The content to insert
    content: str

    # Whether to append the content just to the end of the file, or replace the entire file content.
    append_at_the_end: bool = True


class Outputs(BaseModel):
    # If the file was written to successfully
    success: bool


class WriteIntoFile(Action[Inputs, Outputs]):
    """
    This action writes content into a file.
    """
    id = "write_into_file"

    async def run(self, inputs: Inputs) -> Outputs:
        if os.path.isabs(inputs.filepath):
            raise ValueError(
                f"The filepath: {inputs.filepath} must be relative to the repository root.")

        dirpath = os.path.dirname(inputs.filepath)

        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath)

        with open(inputs.filepath, "a" if inputs.append_at_the_end else "w") as f:
            f.write(inputs.content)
        return Outputs(success=True)


if __name__ == "__main__":
    import os

    from autopr.tests.utils import run_action_manually

    filepath = os.path.join(os.getcwd())
    inputs = Inputs(
        filepath="/ire.txt",
        content="Hello world!",
        append_at_the_end=False,
    )
    outputs = asyncio.run(run_action_manually(
        action=WriteIntoFile, inputs=inputs))

import asyncio

import pydantic

from autopr.actions.base import Action


# The action's inputs
class BashInputs(pydantic.BaseModel):
    command: str


# The action's outputs
class BashOutputs(pydantic.BaseModel):
    stdout: str
    stderr: str


class Bash(Action[BashInputs, BashOutputs]):
    """
    Run a bash command and return its output.
    """

    id = "bash"

    async def run(self, inputs: BashInputs) -> BashOutputs:
        # Get the input value
        command = inputs.command

        # Run the command
        process = await asyncio.create_subprocess_shell(
            command,
            shell=True,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Get standard output and standard error streams
        stdout, stderr = await process.communicate()

        # Set the output values
        return BashOutputs(
            stdout=stdout.decode("utf-8"),
            stderr=stderr.decode("utf-8"),
        )


# When you run this file
if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually
    asyncio.run(
        # Run the action manually
        run_action_manually(
            action=Bash,
            inputs=BashInputs(
                command="echo 'Hello World!'"
            ),
        )
    )

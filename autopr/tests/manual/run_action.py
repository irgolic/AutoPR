import asyncio

from autopr.models.executable import ExecutableId, ContextDict
from autopr.tests.utils import run_action_manually

# ---

# The repo you'd like to run the workflow in (see autopr/tests/repo_resources)
repo_resource = "example_repo_1"

# The action id you'd like to run
action_id = "bash"

# The inputs you'd like to pass to the action
inputs = {"command": "echo 'Hello World!'"}

# ---


outputs = asyncio.run(
    run_action_manually(
        action=ExecutableId(action_id), inputs=ContextDict(inputs), repo_resource=repo_resource
    )
)
print(outputs)

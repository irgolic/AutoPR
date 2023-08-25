import asyncio

from autopr.tests.utils import run_workflow_manually
from autopr.models.executable import ExecutableId, ContextDict

# ---


# The repo you'd like to run the workflow on (see tests/repo_resources)
repo_resource = "example_repo_1"

# The filename of the config file you'd like to use (see tests/configs)
workflows_filename = "bash.yaml"

# The workflow you'd like to run (in the config file)
workflow_id = "bash_workflow"

# The inputs you'd like to pass to the workflow
inputs = {
    "command": "echo 'Hello World!'"
}


# ---


out = asyncio.run(
    run_workflow_manually(
        workflows_filename=workflows_filename,
        workflow_id=ExecutableId(workflow_id),
        inputs=ContextDict(inputs),
        repo_resource=repo_resource,
    )
)

# Print the output
print("Output:")
print(out)

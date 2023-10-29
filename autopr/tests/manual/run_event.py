import asyncio

from autopr.models.events import LabelEvent
from autopr.models.artifacts import Issue, Message
from autopr.tests.utils import create_ephemeral_main_service

# ---


# The filename of the triggers file you'd like to use (see tests/triggers)
triggers_filename = "bash.yaml"

# The filename of the workflows file you'd like to use (see tests/workflows)
workflows_filename = "bash.yaml"

# The event you'd like to run the workflow on
event = LabelEvent(
    pull_request=None,
    issue=Issue(
        number=1,
        title="Test Issue",
        author="Tester",
        timestamp="2021-01-01T00:00:00Z",
        messages=[
            Message(
                body="Test message 1",
                author="Tester",
            ),
        ]
    ),
    label="autopr",
)

repo_resource = "example_repo_1"


# ---


# Initialize
main = create_ephemeral_main_service(
    triggers_filename=triggers_filename,
    workflows_filename=workflows_filename,
    repo_resource=repo_resource,
    event=event,
)

trigger_contexts = main.trigger_service._get_triggers_and_contexts_for_event(event)
trigger_coros = asyncio.run(main.trigger_service._get_trigger_coros_for_event(trigger_contexts))

if trigger_coros:
    # Run the first trigger you find
    out = asyncio.run(trigger_coros[0])
else:
    print("No trigger found for event")
    out = None

# Print the output
print("Output:")
print(out)

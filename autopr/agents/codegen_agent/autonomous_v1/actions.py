from typing import Literal, Optional, Union

from autopr.agents.codegen_agent.autonomous_v1.action_utils.context import ContextFile
from autopr.models.artifacts import Issue
from autopr.models.prompt_rails import PromptRail
from autopr.models.rail_objects import RailObject, PullRequestDescription, CommitPlan


###
# Action decision objects
###


class NewFileAction(RailObject):
    output_spec = f"""<string
    name="filepath"
    description="Path to the newly created file."
    required="true"
/>
<string
    name="description"
    description="Description of the contents of the new file."
    required="true"
/>
"""

    filepath: str
    description: str

    def __str__(self):
        return f"Created file {self.filepath}"


class EditFileAction(RailObject):
    output_spec = f"""<string
    name="filepath"
    description="Path to the file to be edited."
    required="true"
/>
<string
    name="description"
    description="Description of the changes to be made to the file."
    required="true"
/>"""
# <integer
#     name="start_line"
#     description="The line number of the first line of the hunk to be edited."
#     format="positive"
#     required="true"
#     on-fail="noop"
# />
# <integer
#     name="end_line"
#     description="The line number of the last line of the hunk to be edited. Keep the hunk as short as possible while fulfilling the description."
#     format="positive"
#     required="true"
#     on-fail="noop"
# />"""

    filepath: str
    description: str
    # start_line: int
    # end_line: int

    def __str__(self):
        return f"Edited file {self.filepath}"
        # return f"Edited file {self.filepath}:L{self.start_line}-L{self.end_line}"


ActionUnion = Union[NewFileAction, EditFileAction]


###
# Action choice rail
###


class Action(RailObject):
    output_spec = f"""<choice
    name="action"
    on-fail-choice="reask"
>
<case
    name="new_file"
>
<object
    name="new_file"
>
{NewFileAction.output_spec}
</object>
</case>
<case
    name="edit_file"
>
<object
    name="edit_file"
>
{EditFileAction.output_spec}
</object>
</case>
<case
    name="finished"
>
<string
    name="commit_message"
    description="A more appropriate commit message based on the actions taken."
    required="true"
/>
</case>
</choice>"""

    action: Literal["new_file", "edit_file", "finished"]
    new_file: Optional[NewFileAction]
    edit_file: Optional[EditFileAction]
    commit_message: Optional[str]


class MakeDecision(PromptRail):
    two_step = False
    output_type = Action
    prompt_spec = f"""You are about to make a decision on what to do next.

This is the issue that was opened:
```{{issue}}```

This is the pull request we're creating:
```{{pull_request_description}}```

This is the commit we're writing:
```{{commit}}```

This is the codebase subset we decided to look at:
```{{context_hunks}}```

These are the actions we've taken so far:
```{{past_actions}}```

In our pursuit of implementing this commit, please make a decision on what to do next.
If a new file should be created, respond with `new_file` and the file path and description. 
If one of the files in the codebase subset should be edited, respond with `edit_file` and the file path, description, and line numbers of the hunk to edit.
If you're done, respond with `finished` and the commit message describing the past actions."""

    issue: Issue
    pull_request_description: PullRequestDescription
    commit: CommitPlan
    context_hunks: list[ContextFile]
    past_actions: list[tuple[ActionUnion, str]]  # Action and effect

    def get_string_params(self) -> dict[str, str]:
        params = super().get_string_params()
        params["past_actions"] = "\n".join(
            f"{action}: {effect}" for action, effect in self.past_actions
        )
        return params

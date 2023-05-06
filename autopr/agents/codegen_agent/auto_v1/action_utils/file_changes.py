import json
from typing import Optional

import pydantic

from autopr.agents.codegen_agent.auto_v1.action_utils.context import ContextFile, ContextCodeHunk
from autopr.models.artifacts import Issue
from autopr.models.prompt_chains import PromptChain
from autopr.models.prompt_rails import PromptRail

from autopr.models.rail_objects import PullRequestDescription, CommitPlan
from langchain.schema import BaseOutputParser


class GeneratedFileHunk(pydantic.BaseModel):
    contents: str
    outcome: str


class GeneratedHunkOutputParser(BaseOutputParser):
    def parse(self, output: str) -> Optional[GeneratedFileHunk]:
        output_lines = output.split("\n")

        try:
            # Filter through the output until the first ``` is found
            while not output_lines[0].startswith("```"):
                output_lines.pop(0)
            output_lines.pop(0)

            # Find the last ``` line
            reversed_lines = output_lines[::-1]
            while not reversed_lines[0].startswith("```"):
                reversed_lines.pop(0)
            reversed_lines.pop(0)
            lines = reversed_lines[::-1]

            code = "\n".join(lines)

            # Retrieve the JSON
            json_lines = output_lines[len(lines) + 1:]
            try:
                outcome = json.loads("\n".join(json_lines))["outcome"]
            except json.JSONDecodeError:
                outcome = ""
        except:
            # TODO reask to fix the output
            return None
        return GeneratedFileHunk(
            contents=code,
            outcome=outcome,
        )

    def get_format_instructions(self) -> str:
        return """RESPONSE FORMAT INSTRUCTIONS
----------------------------

When responding to me, please use the following format. Make sure you return both the code enclosed in backticks and the JSON immediately after.

```
<string>
```
{
    "outcome": string  # A description of the outcome of the attempt to rewrite the file hunk according to the problem statement.
}
"""


class NewFileChain(PromptChain):
    output_parser = GeneratedHunkOutputParser()
    prompt_template = f"""Hey, we've got a new file to create.

This is the issue that was opened:
```
{{issue}}
```

This is the pull request we're creating:
```
{{pull_request_description}}
```

This is the commit we're writing:
```
{{commit}}
```

This is the codebase subset we decided to look at:
```
{{context_hunks}}
```

This is the plan for the file we're creating:
```
{{plan}}
```

Please send me the contents of the file.

{{format_instructions}}"""

    issue: Issue
    pull_request_description: PullRequestDescription
    commit: CommitPlan
    context_hunks: list[ContextFile]
    plan: str


class RewriteCodeHunkChain(PromptChain):
    output_parser = GeneratedHunkOutputParser()
    prompt_template = f"""Hey, we've got a new code hunk to diff.
    
This is the issue that was opened:
```
{{issue}}
```
    
This is the pull request we're creating:
```
{{pull_request_description}}
```
    
This is the commit we're writing:
```
{{commit}}
```
    
This is the codebase subset we decided to look at:
```
{{context_hunks}}
```
    
This is the hunk we're rewriting:
```
{{hunk_contents}}
```
    
This is the plan for how we want to rewrite the hunk:
```
{{plan}}
```
    
Please rewrite the hunk to match the plan, but do not include any lines prefixed with | in the result.

RULES:
- ONLY rewrite the lines prefixed with *, 
- submit only the lines without the * prefix,
- do not preserve the relative leading indentation of the lines (start the hunk's indentation at 0).
    
{{format_instructions}}"""

    issue: Issue
    pull_request_description: PullRequestDescription
    commit: CommitPlan
    context_hunks: list[ContextFile]
    hunk_contents: ContextCodeHunk
    plan: str

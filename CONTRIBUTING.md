# Contributing to AutoPR

Got an idea on how to improve AutoPR?
Contributions welcome, and greatly appreciated! 🙏

Join [Discord](https://discord.gg/ykk7Znt3K6) to discuss ideas and get help.

## Overview

AutoPR works in two main steps:
- Gather context and plan a pull request
- Generate code for each commit

It's easy to add a new implementation for either of the two steps. 
As long as the file is in the correct directory, it will be automatically picked up by the action – simply refer to it by its id.

## Using a custom component

To use a custom pull request or code generator agent, simply refer to it by its `id` in the action's `with` section.
Make sure you're pointing to the correct branch (in this example `main`).

Example:

`>>> .github/workflows/autopr.yml`
```yaml

...
    - name: AutoPR
      uses: irgolic/AutoPR@main
      with:
        codegen_id: my-codegen
        planner_id: my-pr-agent
...
```

### Adding a new pull request agent

To add a new PR planner, create a new file in `autopr/agents/pull_request_agent/` and subclass `PullRequestAgentBase`. 
The new class should declare an `id` and implement the `_plan_pull_request` method.

Example:

`>>> autopr/agents/planner_agent/my_planner_agent.py`
```python

from typing import Union
from git.repo import Repo
from autopr.agents.pull_request_agent import PullRequestAgentBase
from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription
from autopr.models.events import IssueOpenedEvent


class MyPullRequestAgent(PullRequestAgentBase):
    id = "my-pr-agent"

    def _plan_pull_request(
        self, 
        issue: Issue, 
        repo: Repo,
        event: IssueOpenedEvent,
    ) -> Union[str, PullRequestDescription]:
        return """
Title: My PR title
Body: My PR body
Commits:
  1. Title: My commit title
     Files:
       - path/to/file.py
       - path/to/another/file.py
  2. Title: My second commit title
     Files:
       - path/to/file.py
       - path/to/another/file.py
"""
```

The plan can be returned as a `PullRequestDescription` object, or as a string as shown in the dummy example above.
If it is returned as a string, it will automatically be parsed into a `PullRequestDescription` object with guardrails.


### Adding a new code generator

To add a new code generator, create a new file in `autopr/agents/codegen_agent/` and subclass `CodegenAgentBase`. 
Similarly to the pull request agent, the new class should declare an `id` and implement the `_generate_code` method.

Example:

`>>> autopr/agents/codegen_agent/my_codegen_agent.py`
```python

from autopr.agents.codegen_agent import CodegenAgentBase
from autopr.models.artifacts import Issue, DiffStr
from git.repo import Repo
from autopr.models.rail_objects import CommitPlan, PullRequestDescription

class MyCodegenAgent(CodegenAgentBase):
    id = "my-codegen"

    def _generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> DiffStr:    
        return """
--- /dev/null
+++ dummy.py
@@ -0,0 +1,2 @@
+def dummy():
+    pass
"""
```

The output of the code generator is a string, which must be a valid patch as applicable by GNU `patch`.
We're currently working on a serializable patch format similar to the pull request agent agent's `PullRequestDescription` object.
If you're interested in this, please join our [Discord](https://discord.gg/ykk7Znt3K6).

## How guardrails is used in AutoPR

RailService is a service that runs rails defined in `autopr/models/rails.py`. 
It's accessible by default in PR agents and code generators at `self.rail_service`.
The rails' output models are defined in `autopr/models/rail_objects.py`.

Each rail run consists of two calls:
- one with a raw chat message, talking with the LLM in natural language,
- one with guardrails, asking the LLM to serialize the previous response to a typed JSON object.

Feel free to define your own rails and develop alternate strategies for describing pull requests and generating code. 
Or ignore them altogether and try an approach with a different library.
# Contributing to AutoPR

Got an idea on how to improve AutoPR?
Contributions welcome, and greatly appreciated! 🙏

Join [Discord](https://discord.gg/ykk7Znt3K6) to discuss ideas and get guidance.

## Overview

AutoPR works in two main steps:
- Gather context and plan a pull request
- Generate code for each commit

It's easy to add a new implementation for either of the two steps, or for the orchestration of them. 
As long as the file is in the correct directory, it will be automatically picked up by the action – simply refer to it by its id.
Alternatively, write the agent in its own directory module, just make sure to export it to `__all__` in the `__init__.py` file. 

## Using a custom component

To use a custom brain or pull request or code generator agent, simply refer to it by its `id` in the action's `with` section.
Make sure you're pointing to the correct branch (in this example `main`).

Example:

`>>> .github/workflows/autopr.yml`
```yaml

...
    - name: AutoPR
      uses: irgolic/AutoPR@main
      with:
        codegen_agent_id: my-codegen-agent
        pull_request_agent_id: my-pr-agent
        brain_agent_id: my-brain-agent
...
```

### Brain agents

Brain agents are responsible for handling the "issue labeled" event to generate the pull request, normally by invoking pull request planning and code generating subagents.

To add a new brain agent, create a new file or directory in `autopr/agents/brain_agent/` and subclass `BrainAgentBase`.

Example:

`>>> autopr/agents/brain_agent/my_brain_agent.py`
```python

from autopr.agents.brain_agent import BrainAgentBase
from autopr.models.events import EventUnion

class MyBrainAgent(BrainAgentBase):
    id = "my-brain-agent"

    def _plan_pull_request(
        self, 
        event: EventUnion,
    ) -> None:
        # Get the issue
        issue = event.issue
        # Plan the pull request
        pr_desc = self.pull_request_agent.plan_pull_request(self.repo, issue, event)
        # Generate a change
        self.codegen_agent.generate_changes(
            self.repo,
            issue,
            pr_desc,
            pr_desc.commits[0],
        )
        # Publish the pull request
        self.publish_service.publish(pr_desc)
```

### Pull request agents

To add a new PR planner, create a new file or directory in `autopr/agents/pull_request_agent/` and subclass `PullRequestAgentBase`. 
The new class should declare an `id` and implement the `_plan_pull_request` method.

Example:

`>>> autopr/agents/planner_agent/my_planner_agent.py`
```python

from typing import Union
from git.repo import Repo
from autopr.agents.pull_request_agent import PullRequestAgentBase
from autopr.models.artifacts import Issue
from autopr.models.rail_objects import PullRequestDescription
from autopr.models.events import EventUnion



class MyPullRequestAgent(PullRequestAgentBase):
    id = "my-pr-agent"

    def _plan_pull_request(
        self, 
        issue: Issue, 
        repo: Repo,
        event: EventUnion,
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


### Codegen agents

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
    id = "my-codegen-agent"

    def _generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> None:    
        diff = """
--- /dev/null
+++ dummy.py
@@ -0,0 +1,2 @@
+def dummy():
+    pass
"""
        self.diff_service.apply_diff(diff)
```

A codegen agent is expected to make file changes, either by generating a diff or otherwise.
If you'd like to work on codegen, check out the [autonomous codegen agent](https://github.com/irgolic/AutoPR/tree/main/autopr/agents/codegen_agent/autonomous_v1).


## How guardrails is used in AutoPR

RailService is a service that runs rails defined in `autopr/models/rails.py`. 
It's accessible by default in PR agents and code generators at `self.rail_service`.
The rails' output models are defined in `autopr/models/rail_objects.py`.

Each rail run consists of two calls:
- one with a raw chat message, talking with the LLM in natural language,
- one with guardrails, asking the LLM to serialize the previous response to a typed JSON object.

Feel free to define your own rails and develop alternate strategies for describing pull requests and generating code. 
Or ignore them altogether and try an approach with a different library.
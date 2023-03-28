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

To use a custom defined PR planner or code generator, simply refer to it by its `id` in the action's `with` section.
Make sure you're pointing to the correct branch (in this example `main`).

Example:

```yaml
>>> .github/workflows/autopr.yml

...
    - name: AutoPR
      uses: irgolic/AutoPR@main
      with:
        codegen_id: my-codegen
        planner_id: my-planner
...
```

### Adding a new PR planner

To add a new PR planner, create a new file in `autopr/services/planner_service/` and subclass `PlannerServiceBase`. 
The new class should declare an `id` and implement the `_plan_pr` method.

Example:
```python
>>> autopr/services/planner_service/my_planner_service.py

from autopr.services.planner_service import PlannerServiceBase
from autopr.models.artifacts import Issue
from git.repo import Repo
from autopr.models.rail_objects import PullRequestDescription, CommitPlan


class MyPlannerService(PlannerServiceBase):
    id = "my-planner"

    def _plan_pr(self, issue: Issue, repo: Repo) -> PullRequestDescription:
        commits: list[CommitPlan] = []
        ...
        return PullRequestDescription(
            title="My PR title",
            body="My PR body",
            commits=commits,
        )
``` 


### Adding a new code generator

To add a new code generator, create a new file in `autopr/services/codegen_service/` and subclass `CodegenServiceBase`. 
Similarly to the planner service, the new class should declare an `id` and implement the `_generate_code` method.

Example:
```python
>>> autopr/services/codegen_service/my_codegen_service.py

from autopr.services.codegen_service import CodegenServiceBase
from autopr.models.artifacts import Issue, DiffStr
from git.repo import Repo
from autopr.models.rail_objects import CommitPlan, PullRequestDescription,

class MyCodegenService(CodegenServiceBase):
    id = "my-codegen"

    def _generate_patch(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> DiffStr:    
        example_diff = """
--- /dev/null
+++ dummy.py
@@ -0,0 +1,2 @@
+def dummy():
+    pass
"""
        ...
        return example_diff
```

To use it, set `codegen_id` to `my-codegen` in the AutoPR workflow yml.

## How guardrails is used in AutoPR

RailService is a service that runs rails defined in `autopr/models/rails.py`. 
It's accessible by default in PR planners and code generators at `self.rail_service`.
The rails' output models are defined in `autopr/models/rail_objects.py`.

Each rail run consists of two calls:
- one with a raw chat message, talking with the LLM in natural language,
- one with guardrails, asking the LLM to serialize the previous response to a typed JSON object.

Feel free to define your own rails and develop alternate strategies for describing pull requests and generating code. 
Or ignore them altogether and try an approach with a different library.
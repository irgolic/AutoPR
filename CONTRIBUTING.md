# Contributing to AutoPR

Got an idea on how to improve AutoPR?
Contributions welcome, and greatly appreciated! 🙏

Join [Discord](https://discord.gg/ykk7Znt3K6) to discuss ideas and get guidance.

## Overview

AutoPR is built around two main concepts:
- actions: orthogonal components that perform a specific task
- agents: components that iteratively run actions

Agents orchestrate an action flow to handle an event, such as a label being added to an issue.

## Actions

To write a custom action, subclass `Action`, give it an `id`, and implement the `run` method.

Here's a skeleton of the simplest possible action:

```python
class MyAction(Action):
    id = "my_action"

    def run(self, arguments: Action.Arguments, context: ContextDict) -> ContextDict:
        # do something
        return context
```

You can also give it a description to help the model understand what it does, and define arguments for your action.  
Subclass `Action.Arguments`, declare them as pydantic fields, and write a guardrails `output_spec`.

Here's an example of an action that summarizes an issue:

```python
class SummarizeIssue(Action):
    id = "summarize_issue"
    description = "Summarize the issue into a single sentence."

    class Arguments(Action.Arguments):
        single_sentence_summary: str

        output_spec = "<string name='single_sentence_summary'/>"

    def run(self, arguments: Arguments, context: ContextDict) -> ContextDict:
        context["summary"] = arguments.single_sentence_summary
        return context
```

The context is a dictionary that is passed between actions by the agent, to share information among them.

## Agents

Agents are the main entry point for AutoPR. They are responsible for running actions in response to events.

To write a custom agent, subclass `Agent`, give it an `id`, and implement the `handle_event` method.

```python
class MyAgent(Agent):
    id = "my_agent"

    def __init__(
        self,
        *args,
        my_action_id: str = "my_action",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.my_action_id = my_action_id

    def handle_event(
        self,
        event: EventUnion,
    ) -> None:
        # Initialize the context
        context = ContextDict(
            issue=event.issue,
        )
        
        # Run the action
        context = self.action_service.run_action(self.my_action_id, context)

```

You can pass keyword arguments to your agent via the `autopr.yml` workflow file, for example:

```yaml
...
    - name: AutoPR
      uses: docker://ghcr.io/irgolic/autopr:latest
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        agent_id: my_agent
        agent_config: |
          my_action_id: my_other_action
...
```

Events are the input to agents. They are defined in `autopr/models/events.py`.  
Currently only `IssueLabeledEvent` is supported.

## Services

Actions and agents have access to services that provide useful functionality, such as language model calls (rail_service), or posting updates (publish_service).

TODO overview of services

## How guardrails is used in AutoPR

RailService is a service that runs rails defined in `autopr/models/rails.py`. 
It's accessible by default in PR agents and code generators at `self.rail_service`.
The rails' output models are defined in `autopr/models/rail_objects.py`.

Each rail run consists of two calls:
- one with a raw chat message, talking with the LLM in natural language,
- one with guardrails, asking the LLM to serialize the previous response to a typed JSON object.

Feel free to define your own rails and develop alternate strategies for describing pull requests and generating code. 
Or ignore them altogether and try an approach with a different library.
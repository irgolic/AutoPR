

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files and folders related to a workflow automation system for handling events in the AutoPR system. It includes files for defining data models, handling events, configuring workflows, and executing automation actions. The files define classes and types for messages, threads, issues, pull requests, events, context variables, templates, and executables. Overall, this folder provides a flexible and extensible system for defining and configuring automated actions and workflows in the AutoPR system.


### [`__init__.py`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models/__init__.py)

This file is empty.  


### [`artifacts.py`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models/artifacts.py)

📄 This file contains Python code for defining data models related to messages, threads, issues, and pull requests.   
🧵 The `Message` class represents a message with a body and an author.   
🧵 The `Thread` class represents a collection of messages.   
🧵 The `Issue` class extends the `Thread` class and adds additional properties such as open status, number, title, author, and timestamp.   
🧵 The `PullRequest` class extends the `Issue` class and adds properties specific to pull requests, such as base branch, head branch, and base commit SHA.   
🧵 The `CodeComment` class (currently commented out) extends the `Thread` class and represents code comments with properties like commit SHA, filepath, and status.   
🔧 The file also defines a type alias `DiffStr` for a string representing code diffs.  


### [`config/`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models/config)

This folder contains several Python files that provide a framework for defining and executing workflows with customizable actions and context variables. It includes models for data validation, models and classes for workflows, actions, and context variables, code for building workflow definitions and trigger configurations for an automated PR system, classes for transforming variables between config and action types, and code for handling variables and parameters within a specific context. Overall, this folder provides a flexible and extensible system for defining and configuring automated actions and workflows.  


### [`events.py`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models/events.py)

📄 The file defines several classes related to events in the AutoPR system.   
🔀 The `Event` class is the base class for all events and has a `pull_request` and `issue` attribute.  
🏷️ The `LabelEvent` class represents an event triggered when a label is added to an issue or pull request and has a `label` attribute.  
💬 The `CommentEvent` class represents an event triggered when a comment is added to an issue or pull request and has a `comment` attribute.  
📥 The `PushEvent` class represents an event triggered when a push is made to a branch and has a `branch` attribute.  
⏰ The `CronEvent` class represents an event triggered by a cron job and has a `cron_schedule` attribute.  
🔀 The `EventUnion` type is a union of different event classes.  
🔒 The `CodeReviewEvent` class, which is currently commented out, represents an event triggered when a comment is added to a code review.  
💡 The file uses the `pydantic` library for modeling the data structures.  
🔁 The file may be used to handle and process various types of events in the AutoPR system.  


### [`executable.py`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models/executable.py)

📄 This file defines various types and classes related to context variables, templates, and executables in a workflow automation system.  
📝 Types include LambdaString, ContextVarName, ContextVarPath, TemplateString, and TemplateObject.  
🔍 The ContextDict class provides methods for retrieving values from the context by path and rendering templates.  
⚙️ The file also defines the ControlWords type and the ExecutableId class, which is a string with reserved keywords.  
🔄 There are forward references for different types of executables.  
🧩 The Executable type represents an executable reference or a list of executable references.  
🔒 The StrictExecutable type is similar to Executable but with stricter reference types.  
🔒 StrictExecutableForwardRef is used in the StrictExecutable type.  

<!-- Living README Summary -->
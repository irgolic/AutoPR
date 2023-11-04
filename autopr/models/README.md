

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python code for a workflow automation system called AutoPR. It includes files for defining data models related to messages, threads, issues, and pull requests, as well as files for defining and executing workflows with customizable actions and context variables. There are also classes related to events in the system and types and classes related to context variables, templates, and executables. Overall, this folder provides a comprehensive system for defining, executing, and handling workflows in a Python application.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/__init__.py)

This file is empty.  


### [`artifacts.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/artifacts.py)

📄 This file contains Python code for defining data models related to messages, threads, issues, and pull requests.   
🧵 The `Message` class represents a message with a body and an author.   
🧵 The `Thread` class represents a collection of messages.   
🧵 The `Issue` class extends the `Thread` class and adds additional properties such as open status, number, title, author, and timestamp.   
🧵 The `PullRequest` class extends the `Issue` class and adds properties specific to pull requests, such as base branch, head branch, and base commit SHA.   
🧵 The `CodeComment` class (currently commented out) extends the `Thread` class and represents code comments with properties like commit SHA, filepath, and status.   
🔧 The file also defines a type alias `DiffStr` for a string representing code diffs.  


### [`config/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config)

This folder contains Python code for defining and executing workflows with customizable actions and context variables. The code includes models and classes for workflow structures, actions, context actions, and variable transformations. It also provides frameworks for rendering and evaluating different types of variables within a context, as well as building workflow definitions and triggers. The code uses the Pydantic library for structure and validation, and generates JSON schemas for triggers and workflows. Overall, this folder provides a comprehensive system for defining, executing, and handling workflows in a Python application.  


### [`events.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/events.py)

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


### [`executable.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/executable.py)

📄 This file defines various types and classes related to context variables, templates, and executables in a workflow automation system.  
📝 Types include LambdaString, ContextVarName, ContextVarPath, TemplateString, and TemplateObject.  
🔍 The ContextDict class provides methods for retrieving values from the context by path and rendering templates.  
⚙️ The file also defines the ControlWords type and the ExecutableId class, which is a string with reserved keywords.  
🔄 There are forward references for different types of executables.  
🧩 The Executable type represents an executable reference or a list of executable references.  
🔒 The StrictExecutable type is similar to Executable but with stricter reference types.  
🔒 StrictExecutableForwardRef is used in the StrictExecutable type.  

<!-- Living README Summary -->
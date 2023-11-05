

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files that define models, classes, and declarations for a workflow-based application. It provides a framework for defining and executing workflows, handling variables and parameters, transforming data, and generating JSON schemas. The files enforce strict validation of input data and allow for customizable actions and context variables, providing a flexible and extensible system for building and managing workflows. Additionally, there are files that define classes related to events in the AutoPR system, as well as files that define various types and classes related to context variables, templates, and executables in a workflow automation system.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models/__init__.py)

This file is empty.  


### [`artifacts.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models/artifacts.py)

📄 This file contains Python code for defining data models related to messages, threads, issues, and pull requests.   
🧵 The `Message` class represents a message with a body and an author.   
🧵 The `Thread` class represents a collection of messages.   
🧵 The `Issue` class extends the `Thread` class and adds additional properties such as open status, number, title, author, and timestamp.   
🧵 The `PullRequest` class extends the `Issue` class and adds properties specific to pull requests, such as base branch, head branch, and base commit SHA.   
🧵 The `CodeComment` class (currently commented out) extends the `Thread` class and represents code comments with properties like commit SHA, filepath, and status.   
🔧 The file also defines a type alias `DiffStr` for a string representing code diffs.  


### [`config/`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models/config)

This folder contains various Python files that define models, classes, and declarations for a workflow-based application. The files provide a framework for defining and executing workflows, handling variables and parameters, transforming data, and generating JSON schemas. The models enforce strict validation of input data and allow for customizable actions and context variables. Overall, this folder provides a flexible and extensible system for building and managing workflows.  


### [`events.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models/events.py)

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


### [`executable.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models/executable.py)

📄 This file defines various types and classes related to context variables, templates, and executables in a workflow automation system.  
📝 Types include LambdaString, ContextVarName, ContextVarPath, TemplateString, and TemplateObject.  
🔍 The ContextDict class provides methods for retrieving values from the context by path and rendering templates.  
⚙️ The file also defines the ControlWords type and the ExecutableId class, which is a string with reserved keywords.  
🔄 There are forward references for different types of executables.  
🧩 The Executable type represents an executable reference or a list of executable references.  
🔒 The StrictExecutable type is similar to Executable but with stricter reference types.  
🔒 StrictExecutableForwardRef is used in the StrictExecutable type.  

<!-- Living README Summary -->
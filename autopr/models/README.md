

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files related to an automation system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config/` folder contains files for configuring actions, workflows, and context models. The `events.py` file defines classes for different types of events that can trigger the automation system. The `executable.py` file defines types and classes related to context variables, templates, and executables. Overall, this folder provides a foundation for building a flexible and extensible automation system.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/models/__init__.py)

This file is empty.  


### [`artifacts.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/models/artifacts.py)

📄 This file contains Python code for defining data models related to messages, threads, issues, and pull requests.  
📝 The purpose of the code is to provide a structured way to represent and manipulate these data types.  
💬 The `Message` class represents a single message with a body and an author.  
🧵 The `Thread` class represents a collection of messages, forming a conversation thread.  
🔢 The `Issue` class extends the `Thread` class and adds additional properties like number, title, author, and timestamp.  
🔀 The `PullRequest` class extends the `Issue` class and adds properties specific to pull requests, like base branch and head branch.  
🔒 The `CodeComment` class is commented out, but it represents comments related to code changes in a pull request.  
📝 The `DiffStr` type alias is defined for representing diff strings.  
🗒️ Overall, this file provides a foundation for working with messages, threads, issues, and pull requests in Python.  


### [`config/`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/models/config)

This folder contains files that define and configure actions, workflows, and context models for an automation system. It includes base model classes with different configuration settings, code for building workflow models and trigger configurations, code for transforming between config and action variables, and classes and declarations related to variables and parameters. The files are organized and utilize the Pydantic library for data validation and modeling, providing a foundation for building a flexible and extensible automation system.  


### [`events.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/models/events.py)

📝 This file defines several classes for different types of events in the AutoPR system.  
🔧 The purpose of this file is to provide a structured way to represent and handle different events that can trigger AutoPR.  
🏗️ The main class is `Event`, which serves as a base model for other event types.  
🔖 `LabelEvent` represents an event triggered when a label is added to an issue or pull request.  
💬 `CommentEvent` represents an event triggered when a comment is added to an issue or pull request.  
🚀 `PushEvent` represents an event triggered when a push is made to a branch.  
⏰ `CronEvent` represents an event triggered by a cron job.  
🔄 There is a commented out class `CodeReviewEvent` which represents an event triggered when a comment is added to a code review.  
🔀 `EventUnion` is a type alias that represents a union of different event types.  


### [`executable.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/models/executable.py)

📝 This file defines various types and classes related to context variables, templates, and executables.  
💡 It includes definitions for types like `LambdaString`, `ContextVarName`, `ContextVarPath`, `TemplateString`, and `TemplateObject`.  
🧩 The `ContextDict` class provides methods for accessing values from a nested context dictionary and rendering templates.  
🔀 The `ControlWords` type is a literal type that represents a tuple of control words like "quit", "return", and "continue".  
🔑 The `ExecutableId` class is a string subclass that represents an executable ID, with reserved keywords that cannot be used as IDs.  
🔗 The `ExecutableForwardRef` and `StrictExecutableForwardRef` types are forward references to various executable types.  
🚀 The `Executable` and `StrictExecutable` types represent executables, which can be either single executables or lists of executables.  
💡 Some forward references are currently ignored by Pyright's type checking.  
⚠️ TODO comments indicate areas that need further work or improvement.  
📚 The file also includes imports of external modules like `jinja2` and `pydantic`.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python code files that define models, actions, and configurations for a workflow automation system. It includes files for working with messages, threads, issues, and pull requests, as well as files for handling different types of events that can trigger actions in the system. The purpose of these files is to provide a structured and type-safe way to define and configure workflows, handle transformations between different types, and represent and handle events.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/__init__.py/)

This file is empty.


### [`artifacts.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/artifacts.py/)

📄 This file contains Python code for defining data models related to messages, threads, issues, and pull requests.
📝 The purpose of the code is to provide a structured way to represent and manipulate these data types.
💬 The `Message` class represents a single message with a body and an author.
🧵 The `Thread` class represents a collection of messages, forming a conversation thread.
🔢 The `Issue` class extends the `Thread` class and adds additional properties like number, title, author, and timestamp.
🔀 The `PullRequest` class extends the `Issue` class and adds properties specific to pull requests, like base branch and head branch.
🔒 The `CodeComment` class is commented out, but it represents comments related to code changes in a pull request.
📝 The `DiffStr` type alias is defined for representing diff strings.
🗒️ Overall, this file provides a foundation for working with messages, threads, issues, and pull requests in Python.


### [`config`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/config/)

This folder contains Python code files that define models, actions, and configurations for a workflow automation system. It includes files for handling extra fields in models, defining triggers and workflows, transforming between different representations of IO types, and declaring variables and parameters. The purpose of these files is to provide a structured and type-safe way to define and configure workflows and triggers, handle transformations between different types, and render and evaluate values within a given context.


### [`events.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/events.py/)

📝 This file defines several classes for different types of events in the AutoPR system.
🔧 The purpose of this file is to provide a structured way to represent and handle different events that can trigger AutoPR.
🏗️ The main class is `Event`, which serves as a base model for other event types.
🔖 `LabelEvent` represents an event triggered when a label is added to an issue or pull request.
💬 `CommentEvent` represents an event triggered when a comment is added to an issue or pull request.
🚀 `PushEvent` represents an event triggered when a push is made to a branch.
⏰ `CronEvent` represents an event triggered by a cron job.
🔄 There is a commented out class `CodeReviewEvent` which represents an event triggered when a comment is added to a code review.
🔀 `EventUnion` is a type alias that represents a union of different event types.



### [`executable.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/executable.py/)

📝 This file contains a Python module that defines various types and classes related to context variables, templates, and executable actions.

<!-- Living README Summary -->
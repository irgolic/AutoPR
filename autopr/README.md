

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a diverse collection of files and folders that serve different purposes. It includes actions for autonomous agent systems, reusable components for automation tasks, code for managing prompt context in a chatbot application, logging configuration, implementation of a main service for handling events and triggering actions, models for an AutoPR system, services for managing and running actions within the AutoPR system, trigger configurations, and workflow automation files. Overall, this folder represents a comprehensive set of functionalities and actions that can be used in various automation tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/__init__.py/)

This file is empty.


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/actions/)

This folder contains a collection of Python files that serve different purposes. Some files define base classes and actions for autonomous agent systems, such as performing tasks and making API calls. Other files provide reusable components for running bash commands, generating prompts, reading and writing files, and searching for specific queries in directories. There are also files that implement specific actions, like publishing comments on GitHub issues or setting issue titles. Additionally, there is a folder called "utils" that contains code for managing prompt context in a chatbot application. Overall, this folder represents a diverse set of functionalities and actions that can be used in various automation tasks.


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/gh_actions_entrypoint.py/)

📝 This file is the entry point for a GitHub Actions workflow.
🔧 It imports necessary modules and defines classes for the workflow.
🚀 The purpose of this file is to configure and run the main service for GitHub Actions.
⚙️ It sets up the necessary settings, platform service, and publish service for the workflow.
🔑 It retrieves the required GitHub token and event information from environment variables.
📂 The file also includes functions to get the repository path and load the event data.
🔍 The event data is parsed and returned as an EventUnion object.
📝 The file logs the start of the workflow and runs the main service using asyncio.



### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/log_config.py/)

📝 This file configures logging and sets up a logger for use in the module.


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/main.py/)

📝 The file contains the implementation of a `MainService` class and a `Settings` class. 
📝 The `MainService` class is responsible for handling events and triggering actions based on those events. 
📝 It initializes various services such as `ActionService`, `CommitService`, `PlatformService`, `PublishService`, `TriggerService`, and `WorkflowService`. 
📝 It also defines methods for retrieving repository information, event information, and branch names. 
📝 The `Settings` class defines the configuration settings used by the `MainService` class. 
📝 The `MainService` class has a `run` method that runs the triggers and returns the result. 
📝 The `get_repo_path` method is not implemented and needs to be overridden in subclasses. 
📝 The `get_event` method is not implemented and needs to be overridden in subclasses. 
📝 The `get_platform_service` and `get_publish_service` methods return instances of the `PlatformService` and `PublishService` classes respectively. 
📝 The `get_branch_name` and `get_base_branch_name` methods determine the names of the branch and base branch respectively.


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/)

This folder contains Python code and configuration files for an AutoPR system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config` folder contains files for handling extra fields, defining and executing actions and workflows, building workflow models and triggers, and converting between different representations of IO types. The `events.py` file defines classes for different types of events that can trigger the AutoPR system. The `executable.py` file contains types and classes related to context variables, templates, and executable actions.


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/)

This folder contains a collection of Python files that provide various services and functionalities for managing and running actions within the AutoPR system. These services include a caching service for storing key-value pairs, a commit service for handling Git repository operations, a diff service for getting and applying diffs in a Git repository, a platform service for making API calls to a platform like GitHub, a publish service for publishing updates to a pull request description, a trigger service for handling triggers and executing workflows, a utility module for formatting and truncating nested Python objects, and a workflow service for executing workflows. Each file has a specific purpose and provides functionality that is essential for the AutoPR system.


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/triggers.py/)

📄 This file defines a function called `get_all_triggers`.  
📁 The function takes two parameters: `config_dir` and `repo_path`.  
🔍 It searches for trigger configuration files in the specified directory and subdirectories.  
🔧 The trigger files can have either a `.yaml` or `.yml` extension.  
🔐 It loads the contents of each trigger file using the `yaml` library.  
🔁 If the file is empty or cannot be parsed, it is skipped.  
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.  
🔀 The function returns a list of all triggers extracted from the trigger files.  
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/workflows/)

This folder contains a collection of files related to workflow automation. The `__init__.py` file provides functions for loading and collecting workflows from YAML files. The `api_git_history.yaml` file defines steps for making API calls, saving responses to files, and committing and pushing files to a Git repository. The `autogenerate_readmes.yaml` file contains workflows and actions for generating and formatting summaries for files and folders, and updating README files with the summaries. The `insert_into_readme.yaml` file defines a task for inserting content into a file. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request.

<!-- Living README Summary -->
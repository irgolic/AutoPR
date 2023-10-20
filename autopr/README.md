

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files and subfolders that serve different purposes in an automation system. The "actions" folder contains Python files that define base classes, reusable components, and specific actions for autonomous agent systems. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file configures logging. The "main.py" file is the main entry point for the application and handles triggers and workflows. The "models" folder contains code files that define data models and actions. The "services" folder contains files that provide various services and utility functions. The "triggers.py" file provides a way to retrieve and process trigger configurations. The "workflows" folder contains files related to workflow automation. Overall, this folder represents a diverse set of functionalities and actions that can be used in various automation tasks.


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

📝 This file contains the implementation of the `MainService` class, which is the main entry point for the autopr application. 
🔧 It initializes various services and handles the execution of triggers and workflows based on events received from the platform service. 
🔀 The `run` method triggers the execution of the workflows based on the event received. 
🔧 The `get_repo_path` method needs to be implemented by subclasses. 
🔧 The `get_event` method also needs to be implemented by subclasses and should return the event received from the platform service. 
🔧 The `get_platform_service` method initializes the platform service with the owner and repo name. 
🔧 The `get_publish_service` method initializes the publish service with the platform service, owner, repo name, and other parameters. 
🔧 The `get_branch_name` method generates a branch name based on the event and settings. 
🔧 The `get_base_branch_name` method returns the base branch name based on the event and settings.


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/)

This folder contains Python code files that define data models and actions for a workflow system and an automated PR system. The "artifacts.py" file provides a structured way to represent and manipulate messages, threads, issues, and pull requests. The "config" folder contains files that define models, actions, and transformations for the workflow system. The "events.py" file defines classes for different types of events that can trigger the automated PR system. The "executable.py" file contains types and classes related to context variables, templates, and executable actions.


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/)

This folder contains various Python files that serve different purposes. Some files provide services for managing actions, caching data, handling commits and branches in a Git repository, and interacting with a platform's API. Other files provide utility functions for formatting and truncating nested Python objects and publishing updates to a pull request description. There are also files related to triggers and workflows, as well as a file containing empty initialization code. Each file has a specific role in the overall functionality of the system.


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

This folder contains a collection of files related to workflow automation. The `__init__.py` file provides functions for loading and collecting workflows from YAML files. The `api_git_history.yaml` file defines a workflow for making API calls, saving the response to a file, and pushing it to a Git repository. The `autogenerate_readmes.yaml` file contains workflows for summarizing files and folders and generating README summaries. The `insert_into_readme.yaml` file defines a task for inserting content into a file. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request.

<!-- Living README Summary -->
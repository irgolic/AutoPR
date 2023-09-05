

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that serve different purposes for automation tasks. The "actions" folder contains files that define various actions and utilities for automation, such as running commands, publishing comments, and committing changes. The "models" folder contains files that define models, actions, and configurations for a workflow automation system. The "services" folder contains files that provide services for managing actions, caching, commits, platforms, and workflows. The "workflows" folder contains scripts and files related to workflow configurations. Overall, this folder provides reusable components and configurations for automating different tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/__init__.py/)

This file is empty.


### [`actions`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/actions/)

This folder contains a collection of Python files and a subfolder. The files define various actions and utilities for automation tasks. Each file represents a specific action, such as running a bash command, publishing a comment on a GitHub issue, committing and pushing changes to a remote repository, crawling and filtering the contents of a folder, inserting content into a string, generating prompts using the OpenAI API, reading the contents of a file, setting the title of an issue, and writing content into a file. The subfolder contains a file related to defining and transforming prompt contexts for auto PR generation. Overall, this folder provides a set of reusable components for automating different tasks.


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

📝 This file contains the implementation of the `MainService` class and the `Settings` class. 
🔧 The `MainService` class is the main entry point for running the autopr workflow. 
🔀 It initializes various services such as the `PlatformService`, `PublishService`, `CommitService`, and `ActionService`. 
⚙️ It also handles the creation of branch names, triggering events, and running workflows. 
🔧 The `Settings` class provides default values for various configuration options.


### [`models`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/)

This folder contains Python code files that define models, actions, and configurations for a workflow automation system. It includes files for working with messages, threads, issues, and pull requests, as well as files for handling different types of events that can trigger actions in the system. The purpose of these files is to provide a structured and type-safe way to define and configure workflows, handle transformations between different types, and represent and handle events.


### [`services`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/)

This folder contains various Python files that serve different purposes. Some files provide services for managing actions, caching, commits, diffs, platforms, publishing updates, and workflows. There are also utility functions for formatting and truncating nested objects. These files are part of the AutoPR project and are used for automating pull request actions and managing related tasks.


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


### [`workflows`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/workflows/)

This folder contains Python scripts and YAML files related to workflow configurations. The `__init__.py` script provides functions for loading and collecting workflows from YAML files. The `autogenerate_readmes.yaml` file defines a workflow for generating summaries of files and folders in a directory. The `insert_into_readme.yaml` file defines a task for inserting content into a file using tag-based delimiters. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request.

<!-- Living README Summary -->
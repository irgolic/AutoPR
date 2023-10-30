

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that make up an autonomous agent system. The "actions" folder contains files that define various actions and utilities for the system, such as running commands, making API calls, and generating prompts. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file configures logging. The "main.py" file coordinates services and executes triggers based on events. The "models" folder contains code and configuration files for a larger codebase. The "services" folder provides various services for managing actions, interacting with platforms, and executing workflows. The "triggers.py" file retrieves and processes trigger configurations. The "workflows" folder contains code and YAML files for automating workflows.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions)

This folder contains a collection of Python files that define various actions and utilities for an autonomous agent system. Each file represents a different action or utility, such as running a bash command, making API calls, publishing comments on GitHub issues, generating prompts using OpenAI's GPT-3 language model, and more. These files provide reusable functionality that can be used to perform specific tasks within the autonomous agent system.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/gh_actions_entrypoint.py)

📄 This file is the entry point for a GitHub Actions workflow.    
🔧 It sets up the necessary settings, services, and environment variables.    
🤖 The main purpose is to run the `MainService` class from the `autopr` package.    
🎯 It retrieves the necessary information from the environment variables.    
📝 The `get_event` method loads and extracts the event data for processing.    
🔑 The `get_platform_service` and `get_publish_service` methods create the necessary service instances.    
📂 The `get_repo_path` method retrieves the path to the GitHub workspace.    
📝 The `run` method of `MainService` is called to start the workflow.    
🚀 The file is executed when the script is run directly.  


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/log_config.py)

📝 This file configures logging and sets up a logger for use in the module.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/main.py)

📄 This file contains the implementation of the `MainService` class.  
🔧 The `MainService` class is responsible for coordinating various services and executing triggers based on events.  
🔒 It initializes the necessary services and sets up the configuration for the autopr tool.  
🛠️ It uses the `ActionService`, `CommitService`, `PlatformService`, `PublishService`, `TriggerService`, and `WorkflowService` to perform actions related to pull requests and issues.  
🌐 The `MainService` class interacts with the Git repository, retrieves event information, and creates branches for pull requests.  
🔗 It connects to the platform service (e.g., GitHub) to retrieve data and perform actions on the repository.  
📦 The `MainService` class uses other classes and modules within the project, such as `Settings`, `EventUnion`, and various service classes.  
⚙️ The `run` method triggers the execution of the configured triggers based on the received event.  
🔍 The file also defines helper methods for retrieving repository information and generating branch names.  


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/models)

This folder contains Python code and configuration files related to a larger codebase. The "artifacts.py" file defines data models for messages, threads, issues, and pull requests. The "config/" folder contains files for automation and configuration management. The "events.py" file defines classes for different types of events. The "executable.py" file provides reusable types and classes for managing context and executing actions in a Python project.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services)

This folder contains several Python files that provide various services for managing and running actions, caching data, working with commits and diffs in a Git repository, interacting with platforms like GitHub, publishing updates to pull requests, handling triggers, and executing workflows. These files define classes and methods that encapsulate the functionality related to each service, and they import other modules and dependencies as needed. The files are well-documented with comments explaining the purpose and functionality of each component.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.    
📁 The function takes two parameters: `config_dir` and `repo_path`.    
🔍 It searches for trigger configuration files in the specified directory and subdirectories.    
🔧 The trigger files can have either a `.yaml` or `.yml` extension.    
🔐 It loads the contents of each trigger file using the `yaml` library.    
🔁 If the file is empty or cannot be parsed, it is skipped.    
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.    
🔀 The function returns a list of all triggers extracted from the trigger files.    
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.  


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/workflows)

This folder contains Python code and YAML files for automating various workflows. The `__init__.py` file collects and loads workflows from YAML files in a given folder and its subfolders. The `api_git_history.yaml` file defines a series of steps for making an API call, saving the response to a file, and committing and pushing the file to a Git repository. The `autogenerate_readmes.yaml` file contains workflows for generating and updating README summaries for files and folders. The `insert_into_readme.yaml` file defines an action for inserting content into a file. The `list_and_publish_todos.yaml` file updates TODO issues based on specified language and keywords. The `summarize_pr.yaml` file summarizes changes in a pull request and posts the summary as a comment.  

<!-- Living README Summary -->
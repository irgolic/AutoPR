

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders related to an autonomous agent system. The "actions" folder contains various Python files that implement different actions for the system, such as running commands, generating choices, and making API calls. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow and handles the execution of the workflow. The "log_config.py" file is used to configure logging settings. The "main.py" file serves as the main entry point for the application and handles triggers and workflows. The "models" folder contains data models for messages, issues, and pull requests. The "services" folder contains implementations of different services for a pull request workflow system. The "triggers.py" file retrieves trigger configurations from specified files. The "workflows" folder contains YAML files that define different workflows for automation.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/actions)

This folder contains a collection of Python files that implement various actions for an autonomous agent system. These actions include running bash commands, generating choices based on user prompts, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, inserting content into a string at a specified delimiter, listing files and subfolders in a directory, making API calls, generating string prompts, publishing or updating issues on a platform, reading the contents of a file, setting the title of an issue, and writing content into a file. There are also utility files for managing prompt context and listing files in a folder.  


### [`gh_actions_entrypoint.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/gh_actions_entrypoint.py)

📄 This file is the entry point for a GitHub Actions workflow.   
🔧 It contains the main logic for running the workflow.  
🔒 It retrieves settings and authentication tokens from environment variables.  
📥 It loads and parses the event data from a JSON file.  
🚀 It initializes and runs the main service for the GitHub Actions workflow.  
📝 It uses classes and methods from the "autopr" module to handle the workflow.  
⚙️ The purpose of this file is to orchestrate the execution of the workflow.  
🔗 It connects different services, such as the platform service and the publish service.  
🔄 It interacts with the GitHub API to perform actions on the repository.  
🔒 The GitHub token is used for authentication and authorization.  


### [`log_config.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/main.py)

📋 This file contains the implementation of the `MainService` class, which serves as the main entry point for the application.   
🔧 It initializes various services and handles the execution of triggers and workflows.  
📦 It also defines the `Settings` class for storing configuration settings.  
🔍 The `MainService` class retrieves repository information, creates necessary services, and runs triggers based on events.  
✨ Triggers are defined in the `triggers` module, and workflows are defined in the `workflows` module.  
🚀 The `run` method of the `MainService` class triggers the event and executes the associated workflows.  
🌐 The platform-specific functionality is encapsulated in the `PlatformService` class.  
💻 The `ActionService` class handles actions to be performed based on triggers.  
📝 The `CommitService` class manages commits to the repository.  
🔗 The `TriggerService` class handles the interaction between triggers, workflows, and the commit service.  


### [`models/`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/models)

This folder contains files and a subfolder related to a Python application for workflow automation. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config/` subfolder contains files that define models, classes, and declarations for working with workflows and context variables. The `events.py` file defines classes for different types of events in the application. The `executable.py` file defines types and classes related to context variables, templates, and executables in the workflow automation system. Overall, these files provide the structure, functionality, and data modeling for the application's workflows and event handling.  


### [`services/`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/services)

This folder contains multiple Python files that are part of an automated pull request (PR) workflow system. The files include implementations of various services such as `ActionService`, `CacheService`, `CommitService`, `DiffService`, `PlatformService`, `PublishService`, `TriggerService`, `Utils`, and `WorkflowService`. These services handle different aspects of the PR workflow, such as managing and running actions, caching data, interacting with Git repositories, applying and getting diffs, interacting with platforms like GitHub, publishing updates to PR descriptions, handling triggers and events, formatting and truncating data, and executing workflows based on their IDs. The code is well-documented and organized, with clear separation of concerns.  


### [`triggers.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.  
📂 It imports necessary modules and classes.  
💡 The purpose of this function is to retrieve all trigger configurations from specified files.  
🗂️ It searches for trigger configurations in a given directory.  
🔍 The function looks for trigger configurations in both YAML and YML file formats.  
📝 It reads the contents of the trigger configuration files.  
🧪 The function validates and parses the trigger configurations using Pydantic.  
🔀 It extracts the triggers from the parsed configurations.  
🔄 The function returns a list of all triggers found in the trigger configuration files.  
📥 The function takes optional parameters for the configuration directory and repository path.  


### [`workflows/`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows)

This folder contains a collection of YAML files that define different workflows. These workflows automate various tasks such as making API calls, generating summaries for files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. The files provide configuration and steps for executing these workflows, allowing for customization and automation of these tasks.  

<!-- Living README Summary -->
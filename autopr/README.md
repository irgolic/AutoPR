

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that make up an autonomous agent system. The "actions" folder contains reusable actions for automated processes or scripts, while the "gh_actions_entrypoint.py" file orchestrates the execution of a GitHub Actions workflow. The "log_config.py" file configures logging settings, and the "main.py" file serves as the main entry point for the application. The "models" folder provides code and configuration files for building and executing workflows, and the "services" folder contains classes and services for managing and running actions. The "triggers.py" file retrieves trigger configurations, and the "workflows" folder contains YAML files that define various automation processes.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/actions)

This folder contains a collection of Python files that implement various actions for an autonomous agent system. Each file represents a different action, such as running a bash command, generating choices, publishing comments on GitHub issues, committing and pushing changes to a remote repository, and more. The files define classes that encapsulate the logic for each action, and they often include input and output models for data validation. Additionally, there are utility files for managing prompt context, listing files and subfolders, and performing file operations like reading and writing. Overall, this folder provides a range of reusable actions that can be used in automated processes or scripts.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/main.py)

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


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/models)

This folder contains Python code and configuration files for building and executing workflows in the AutoPR system. It includes files for defining data models related to messages, threads, issues, and pull requests, as well as files for handling events, context variables, templates, and executables. The folder provides the framework and tools for defining, executing, and managing workflows with customizable actions and context variables.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/services)

This folder contains a collection of Python files that together make up a system for managing and running actions in an automated pull request workflow. The files define classes and services for handling actions, caching, commits, diffs, platforms (specifically GitHub), publishing, triggers, utilities, and workflows. Each file serves a specific purpose within the system and provides the necessary functionality for its respective area of responsibility.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/9694ba96863cc48471c71517737ee830784e6688/./autopr/workflows)

This folder contains a collection of YAML files that define various workflows and tasks. The files outline different automation processes, such as making API calls, generating summaries of files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. These workflows can be executed using a workflow management system to automate and streamline these tasks. The files provide clear instructions and configurations for each workflow, allowing for customization and extension to fit specific needs.  

<!-- Living README Summary -->
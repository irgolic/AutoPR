

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and subfolders that provide functionality for managing and automating tasks in an autonomous agent system. The files include actions and utilities for tasks such as running commands, generating choices, publishing comments, committing and pushing changes, searching for keywords, and more. There are also files for configuring logging settings, defining triggers and workflows, defining data models, implementing services for managing actions, and automating workflow processes. Overall, this folder provides a set of reusable components for automating tasks in different contexts.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions)

This folder contains a collection of Python files and a subfolder. The files define various actions and utilities for performing tasks in an autonomous agent system. These actions include tasks such as running Bash commands, generating choices based on user prompts, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, and more. The subfolder contains a file that provides functionality for managing prompt context in a conversational AI system. Overall, the files in this folder provide a set of reusable actions and utilities for automating tasks in different contexts.  


### [`gh_actions_entrypoint.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/main.py)

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


### [`models/`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/models)

This folder contains Python files and a subfolder related to a workflow automation system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config/` subfolder contains files that define the structure and behavior of the application, including models for workflows, actions, and context variables. The `events.py` file defines classes for different types of events in the system. The `executable.py` file defines various types and classes related to context variables, templates, and executables in the workflow automation system.  


### [`services/`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/services)

This folder contains various Python files that implement different services and classes for managing and running actions in an automated PR workflow. These services include the `ActionService` for managing and executing actions, the `CacheService` for caching key-value pairs, the `CommitService` for managing commits and branches in a Git repository, the `DiffService` for getting and applying diffs, the `PlatformService` for interacting with the GitHub platform, the `PublishService` for publishing updates to a pull request description, the `TriggerService` for handling triggers and executing workflows, the `WorkflowService` for executing workflows and actions, and some utility functions for formatting and truncating data for publishing.  


### [`triggers.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows)

This folder contains a collection of Python scripts and YAML configuration files for managing and automating workflows. The scripts and configurations are designed to handle tasks such as collecting and loading workflow configurations from YAML files, making API calls and committing changes to a git repository, generating summaries for files and folders, inserting content into files, finding and publishing TODOs in code, and summarizing changes in a pull request. These files provide a flexible and customizable way to automate various workflow processes.  

<!-- Living README Summary -->
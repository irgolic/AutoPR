

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that implement various functionalities for a workflow automation system. It includes files for managing triggers and workflows, performing actions on a GitHub repository, configuring logging settings, defining data models, and executing customizable workflows. The services folder contains classes for handling different aspects of the workflow, such as caching data, managing commits, interacting with the GitHub platform, and publishing updates to pull requests. The actions folder includes files that define classes and functions for performing specific actions, such as running commands, generating choices, and making API calls. The workflows folder contains YAML files that define different automated tasks and actions.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/actions)

This folder contains various Python files that implement different actions and utilities. These files define classes and functions for performing actions such as running Bash commands, generating choices, publishing comments on GitHub, committing and pushing changes to a remote repository, finding TODOs in code, inserting content into a text, listing files and subfolders, making API calls, generating prompts, publishing or updating issues, reading file contents, searching for specific queries in files, setting issue titles, and writing content into files. The folder also includes a file for managing and manipulating prompt context in a conversational AI system.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/main.py)

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


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models)

This folder contains Python code for a workflow automation system called AutoPR. It includes files for defining data models related to messages, threads, issues, and pull requests, as well as files for defining and executing workflows with customizable actions and context variables. There are also classes related to events in the system and types and classes related to context variables, templates, and executables. Overall, this folder provides a comprehensive system for defining, executing, and handling workflows in a Python application.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services)

This folder contains various Python files that implement different services and classes for managing and running actions in an automated pull request (PR) workflow. These services include the ActionService, CacheService, CommitService, DiffService, PlatformService, PublishService, TriggerService, and WorkflowService. Each service has its own specific purpose, such as handling actions, caching data, managing commits, applying and getting diffs, interacting with the GitHub platform, publishing updates to PRs, handling triggers and executing workflows, and providing utility functions for formatting and truncating data. The files also include subclasses and helper functions to support the main functionality of each service.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/workflows)

This folder contains a collection of YAML files that define various workflows and tasks. These workflows and tasks are designed to automate different actions, such as making API calls, generating summaries of files and folders, inserting content into files, finding and publishing TODOs, and summarizing changes in pull requests. The files provide a flexible and customizable way to configure and execute these actions, and can be extended or modified as needed.  

<!-- Living README Summary -->
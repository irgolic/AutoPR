

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders related to automating tasks and workflows. It includes files for actions and utilities, an entry point for GitHub Actions, logging configuration, the main service for running triggers and workflows, models for building and executing workflows, services for managing actions and Git operations, trigger configurations, and scripts and configuration files for managing workflows. These files and folders provide functionality for automating tasks, interacting with the GitHub platform, and executing customizable workflows.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/actions)

This folder contains a collection of Python files that implement various actions and utilities for automating tasks. The files define classes and functions for actions such as running bash commands, generating choices, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, inserting content into text, listing files and subfolders in a directory, making API calls, generating prompts, publishing or updating issues on a platform, reading file contents, setting issue titles, and writing content into files. The folder also includes a utility for managing and manipulating prompt context in a conversational AI system.  


### [`gh_actions_entrypoint.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/main.py)

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


### [`models/`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/models)

This folder contains Python files that define models, classes, and declarations for building and executing workflows in the AutoPR system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `events.py` file defines classes for different types of events in the system. The `executable.py` file defines types and classes related to context variables, templates, and executables in a workflow automation system. The `config` folder contains files that provide a framework for defining the structure and validation rules for data, handling workflows, actions, triggers, and context information, enabling customizable workflows with configurable actions and context variables.  


### [`services/`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services)

This folder contains a collection of Python files that implement various services and classes for managing and running actions in an automated PR workflow. These services include the `ActionService` for finding, instantiating, and running actions, the `CacheService` for storing and retrieving key-value pairs in a cache directory, the `CommitService` for handling Git-related operations, the `DiffService` for getting and applying diffs, the `PlatformService` for interacting with the GitHub platform, the `PublishService` for publishing updates to a pull request description, the `TriggerService` for handling triggers for events, the `Utils` module for formatting and truncating data, and the `WorkflowService` for executing workflows and actions based on their IDs.  


### [`triggers.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows)

This folder contains a collection of Python scripts and YAML configuration files for managing various workflows. The scripts are designed to collect and load workflow configurations from YAML files, handle exceptions and log errors, and perform operations such as making API calls, generating summaries of files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. The files are well-documented and can be extended or modified to fit specific workflow configuration needs.  

<!-- Living README Summary -->
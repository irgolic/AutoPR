

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders related to an autonomous agent system. The "actions" folder contains Python files that define various actions for the system, such as importing modules, running commands, and making API calls. The "gh_actions_entrypoint.py" file serves as the entry point for a GitHub Actions workflow, orchestrating the workflow execution and interacting with the GitHub API. The "log_config.py" file configures logging settings and creates loggers. The "main.py" file implements the main entry point for the application, handling triggers and workflows. The "models" folder contains files for defining workflows and data models. The "services" folder includes services for managing actions, interacting with the GitHub platform, and executing workflows. The "triggers.py" file retrieves trigger configurations from specified files. The "workflows" folder contains scripts and configuration files for various workflow-related tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/actions)

This folder contains various Python files that define actions for an autonomous agent system. The files provide functionality such as importing modules, running bash commands, generating choices, publishing comments on GitHub issues, committing and pushing changes to a remote repository, finding TODO comments in files, inserting content into text, listing files in a folder, making API calls, generating prompts, publishing or updating issues on a platform, reading file contents, searching for a query in files, setting issue titles, managing prompt context, walking files in a folder, and writing content into files. Each file includes a description of its purpose and usage.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/main.py)

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


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/models)

This folder contains Python files that define and configure workflows for an automated process. It includes files for defining data models related to messages, threads, issues, and pull requests, as well as files for handling events in the system. There are also files for defining and executing customizable workflows with strict validation and flexible variable handling.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services)

This folder contains several Python files that make up a set of services for managing and running actions in an automated pull request workflow. These services handle tasks such as caching, committing changes, applying diffs, interacting with the GitHub platform, and publishing updates to pull request descriptions. There is also a service for executing workflows and handling triggers based on events. Additionally, there are some utility functions for formatting and truncating data for publishing. The code is well-documented and includes import statements and type annotations.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/workflows)

This folder contains Python scripts and YAML configuration files that are used for various workflow-related tasks. The scripts are designed to collect and load workflow configurations from YAML files, handle exceptions and log errors, and provide functions for interacting with APIs, generating README summaries, inserting content into files, managing TODO issues, and summarizing changes in pull requests. The YAML configuration files define the inputs, outputs, and steps for each workflow, and can be extended or modified to fit specific workflow configuration needs.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files and subfolders related to an autonomous agent system. The "actions" folder contains Python files that define various actions and utilities for the system. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file is used to configure logging settings. The "main.py" file contains the implementation of the main service for the application. The "models" folder contains files that define models and classes for the application. The "services" folder contains Python files that provide functionality for managing and running actions in an automated workflow. The "triggers.py" file defines a function for retrieving trigger configurations. The "workflows" folder contains scripts and YAML files that define various workflows for the system.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/actions)

This folder contains various Python files that define different actions and utilities for an autonomous agent system. These actions include tasks such as running Bash commands, generating choices, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, and more. The files are organized into classes and modules that provide reusable functionality for performing these actions. Additionally, there are utility files for managing prompt context in a conversational AI system and for listing files and subfolders in a directory.  


### [`gh_actions_entrypoint.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/main.py)

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


### [`models/`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/models)

This folder contains files that define models, classes, and declarations for a workflow-based application. It provides a framework for defining and executing workflows, handling variables and parameters, transforming data, and generating JSON schemas. The files enforce strict validation of input data and allow for customizable actions and context variables, providing a flexible and extensible system for building and managing workflows. Additionally, there are files that define classes related to events in the AutoPR system, as well as files that define various types and classes related to context variables, templates, and executables in a workflow automation system.  


### [`services/`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/services)

This folder contains several Python files that provide functionality for managing and running actions in an automated pull request (PR) workflow. The files include implementations of classes for services such as `ActionService`, `CacheService`, `CommitService`, `DiffService`, `PlatformService`, `PublishService`, `TriggerService`, `WorkflowService`, as well as some utility functions in `utils.py`. These classes handle tasks such as finding and running actions, caching data, committing changes to a Git repository, applying and getting diffs, interacting with a platform like GitHub, publishing updates to a PR, handling triggers and executing workflows, and formatting and truncating data for publishing. The codebase is well-documented and includes comments explaining the purpose and functionality of each method.  


### [`triggers.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows)

This folder contains a collection of Python scripts and YAML files that serve various purposes. The `__init__.py` script collects and loads workflow configurations from YAML files, handling exceptions and logging errors. The YAML files define workflows for tasks such as making API calls, summarizing files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. These files provide reusable functionality that can be customized and extended to fit specific workflow configuration needs.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and directories that provide various actions, services, workflows, and configurations for automating tasks in a pull request workflow. The files include actions for running commands, generating choices, publishing comments on GitHub issues, committing changes, searching for keywords, making API calls, and more. There are also files for managing logging, defining triggers and workflows, configuring services, and defining data models. The directories contain additional files for managing and running actions, defining workflows, and handling events. Overall, this folder provides a comprehensive set of tools and functionalities for automating tasks in a pull request workflow.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/actions)

This folder contains a collection of Python files that provide various actions and functionalities for automating tasks. The files include actions for running bash commands, generating choices, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, inserting content into text, listing files and subfolders in a directory, making API calls, generating prompts using OpenAI's language model, publishing or updating issues on a platform, reading file contents, setting issue titles, and more. There are also utility files for managing and manipulating prompt context, as well as for listing and filtering files and subfolders.  


### [`gh_actions_entrypoint.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/main.py)

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


### [`models/`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models)

This folder contains Python files that define data models, workflows, and events for the AutoPR system. The `artifacts.py` file defines data models for messages, threads, issues, pull requests, and code comments. The `config/` folder provides a framework for defining and executing workflows with customizable actions and context variables. The `events.py` file defines classes for different types of events in the system. The `executable.py` file defines types and classes related to context variables, templates, and executables in a workflow automation system.  


### [`services/`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/services)

This folder contains the implementation of various services and classes for managing and running actions in an automated pull request workflow. These services include the ActionService, CacheService, CommitService, DiffService, PlatformService, PublishService, TriggerService, and WorkflowService. These classes handle tasks such as finding, instantiating, and running actions, managing caching, managing commits and branches in a Git repository, applying and getting diffs, interacting with the GitHub platform, publishing updates to pull requests, handling triggers and executing workflows, and formatting and truncating data for publishing. There are also some helper functions for resolving input values and formatting outputs.  


### [`triggers.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows)

This folder contains a collection of files that define workflows for various tasks. These tasks include collecting and loading workflow configurations from YAML files, making API calls and committing changes to a git repository, summarizing files and folders and generating README summaries, inserting content into files, managing and publishing TODO issues, and summarizing changes in a pull request. Each file provides a description of its purpose and the steps involved in the workflow it defines. The files can be extended or modified to fit specific needs and rely on other modules and classes imported at the beginning of each file.  

<!-- Living README Summary -->
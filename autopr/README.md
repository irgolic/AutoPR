

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders related to a workflow automation system. It includes files for defining actions, triggers, and workflows, as well as services for managing and running automated actions. There are also files for configuring logging settings, defining data models, and interacting with the GitHub platform. Overall, this folder provides a range of reusable actions, triggers, and workflows for different automation scenarios, along with the necessary services and utilities to support them.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/actions)

This folder contains a collection of Python files that implement various actions for automating tasks. Each file represents a different action, such as running a bash command, generating choices based on user prompts, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, inserting content into strings, and more. The files define classes that encapsulate the logic for each action, and they often include input and output models for data validation. Some files also include example usage and test cases. Additionally, there are utility files for managing prompt context and listing files in a folder. Overall, the folder provides a range of reusable actions for different automation scenarios.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/main.py)

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


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/models)

This folder contains files and folders related to a workflow automation system for handling events in the AutoPR system. It includes files for defining data models, handling events, configuring workflows, and executing automation actions. The files define classes and types for messages, threads, issues, pull requests, events, context variables, templates, and executables. Overall, this folder provides a flexible and extensible system for defining and configuring automated actions and workflows in the AutoPR system.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/services)

This folder contains a collection of Python files that implement various services and classes for managing and running automated actions in a pull request workflow. These services include the `ActionService` for handling actions, the `CacheService` for caching data, the `CommitService` for managing Git commits, the `DiffService` for working with diffs, the `PlatformService` for interacting with the GitHub platform, the `PublishService` for publishing updates to pull requests, the `TriggerService` for handling triggers and executing workflows, the `Utils` module for formatting and truncating data, and the `WorkflowService` for executing workflows and actions. Each file contains detailed documentation and comments explaining the purpose and functionality of the classes and methods.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows)

This folder contains a Python script (`__init__.py`) that collects and loads workflow configurations from YAML files. The script recursively searches for YAML files in a specified folder and its subfolders. It handles exceptions and logs errors during the loading and validation process. The loaded workflows are returned as the result of the `get_all_workflows()` function. The folder also includes several YAML files that define different workflows for tasks such as making API calls and saving responses to files, automating the process of summarizing files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests.  

<!-- Living README Summary -->
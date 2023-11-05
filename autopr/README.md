

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that make up an autonomous agent system. The "actions" folder contains various Python files that define different actions for the system, such as running commands and making API calls. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file is used to configure logging settings. The "main.py" file contains the main entry point for the application, handling triggers and workflows. The "models" folder contains data models and event handling definitions. The "services" folder contains implementations of classes for managing actions and interacting with platforms. The "triggers.py" file retrieves trigger configurations. The "workflows" folder contains YAML configuration files that define various workflows.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/actions)

This folder contains various Python files that define different actions for an autonomous agent system. These actions include running bash commands, generating choices based on user prompts, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, inserting content into text at a specified delimiter, listing files and subfolders in a directory, making API calls, generating string prompts using OpenAI's GPT-3.5 Turbo model, publishing or updating issues on a platform, reading the contents of a file, setting the title of an issue, and writing content into a file. The folder also includes utility files for managing prompt context in a conversational AI system and listing files and subfolders in a directory.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/gh_actions_entrypoint.py)

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


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/log_config.py)

📝 This file is used to configure logging settings and create loggers.   
🔧 It imports the necessary modules for logging and structlog.   
🔒 The logging level is set to DEBUG.   
🎨 If the "pretty" flag is True, additional processors are added for log level, exception info, and console rendering with colors.   
🔧 Otherwise, no processors are added.   
🔧 The structlog is configured with the chosen processors and the logger is cached on first use.   
📝 The file also includes a function to get a logger instance.   
🔧 The configure_logging function is called to configure logging on module import.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/main.py)

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


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/models)

This folder contains Python files that define data models, workflows, and event handling for an automation system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config/` folder contains files that define models, classes, and declarations for workflows, actions, and variables. The `events.py` file defines classes related to events in the system, such as label events, comment events, push events, and cron events. The `executable.py` file defines types and classes related to context variables, templates, and executables in the automation system.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/services)

This folder contains various Python files that together form a PR workflow automation system. The files include implementations of classes for managing and running actions, caching data, committing changes to a Git repository, applying and getting diffs, interacting with platforms like GitHub, publishing updates to a pull request description, handling triggers and executing workflows, formatting and truncating data for publishing, and executing workflows and actions based on their IDs. The files are well-documented and include comments explaining the purpose and functionality of each method.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/triggers.py)

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


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows)

This folder contains a collection of YAML configuration files that define various workflows. These workflows include tasks such as collecting and loading workflow configurations from YAML files, making API calls and saving responses to files, generating summaries of files and folders, inserting content into files, listing and updating TODO issues in code, and summarizing changes in pull requests. These workflows can be run as standalone programs or integrated into other systems to automate and streamline various tasks.  

<!-- Living README Summary -->
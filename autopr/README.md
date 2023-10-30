

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files and subfolders related to an automated pull request workflow system. The "actions" folder contains Python files that define various actions, such as making API calls or generating prompts. The "models" folder contains code and configuration files for managing data models. The "services" folder contains files that implement different services and functionalities for the system. The "triggers.py" file provides a way to retrieve and process trigger configurations. The "workflows" folder contains files for managing and organizing workflows. Overall, these files and folders provide the necessary components for automating pull request workflows in a Python program.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/actions)

This folder contains various Python files that define actions for an autonomous agent system. Each file represents a specific action, such as running a bash command, making an API call, publishing a comment on GitHub, searching files, generating prompts using GPT-3, and more. The files include classes and functions that define the behavior and inputs/outputs of each action. Some files also include test cases for manual execution and validation. Overall, these files provide reusable actions that can be used to automate tasks in a Python program.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/gh_actions_entrypoint.py)

📄 This file is the entry point for a GitHub Actions workflow.    
🔧 It sets up the necessary settings, services, and environment variables.    
🤖 The main purpose is to run the `MainService` class from the `autopr` package.    
🎯 It retrieves the necessary information from the environment variables.    
📝 The `get_event` method loads and extracts the event data for processing.    
🔑 The `get_platform_service` and `get_publish_service` methods create the necessary service instances.    
📂 The `get_repo_path` method retrieves the path to the GitHub workspace.    
📝 The `run` method of `MainService` is called to start the workflow.    
🚀 The file is executed when the script is run directly.  


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/log_config.py)

📝 This file configures logging and sets up a logger for use in the module.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/main.py)

📝 This file contains the implementation of the `MainService` class, which serves as the main entry point for running a series of triggers and workflows in an automated pull request workflow.  
🔧 It also defines the `Settings` class, which holds various configuration settings for the workflow.  
📂 The file imports necessary modules and classes from other files within the project.  
🔀 The `MainService` class initializes and configures various services and utilities required for the workflow, such as the commit service, action service, trigger service, and workflow service.  
🔄 The `run` method of the `MainService` class triggers the execution of the defined triggers and workflows.  
🔧 The file also contains several helper methods for retrieving repository information, event details, platform services, and branch names.  
🚀 The purpose of this file is to provide a centralized and organized implementation for orchestrating the automated pull request workflow.  
⚙️ It is intended to be used as part of a larger system or application that automates the process of creating and managing pull requests based on specified triggers and workflows.  
📖 The file serves as a starting point for understanding the overall structure and logic of the automated pull request workflow.  


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/models)

This folder contains Python code and configuration files related to a larger codebase. The "artifacts.py" file defines data models for messages, threads, issues, and pull requests. The "config/" folder contains files for automation and configuration management. The "events.py" file defines classes for different types of events. The "executable.py" file provides reusable types and classes for managing context and executing actions in a Python project.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/services)

This folder contains various Python files that implement different services and functionalities for the autopr system. These files include classes for managing and running actions, caching data, committing changes to Git repositories, applying and managing diffs, interacting with platforms like GitHub, publishing updates to pull request descriptions, handling triggers and workflows, and providing utility functions for formatting and preparing data. Each file contains detailed documentation and comments explaining the purpose and functionality of the classes and methods.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.    
📁 The function takes two parameters: `config_dir` and `repo_path`.    
🔍 It searches for trigger configuration files in the specified directory and subdirectories.    
🔧 The trigger files can have either a `.yaml` or `.yml` extension.    
🔐 It loads the contents of each trigger file using the `yaml` library.    
🔁 If the file is empty or cannot be parsed, it is skipped.    
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.    
🔀 The function returns a list of all triggers extracted from the trigger files.    
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.  


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows)

This folder contains a collection of files related to managing and organizing workflows. The `__init__.py` file contains functions for loading and collecting workflows from YAML files. The `api_git_history.yaml` file defines steps for making API calls, saving responses, and pushing to a Git repository. The `autogenerate_readmes.yaml` file contains workflows for generating and updating README summaries. The `insert_into_readme.yaml` file defines an action for inserting content into a file. The `list_and_publish_todos.yaml` file automates the process of managing and updating TODOs as GitHub issues. The `summarize_pr.yaml` file summarizes changes in a pull request.  

<!-- Living README Summary -->
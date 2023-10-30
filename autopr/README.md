

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files and folders related to an automated pull request workflow. It includes a set of reusable actions for different tasks, such as running commands, making API calls, and generating prompts. There are also files for managing logging, defining triggers, orchestrating workflows, and handling configuration and models. The folder provides a centralized and organized implementation for automating the process of creating and managing pull requests based on specified triggers and workflows.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/actions)

This folder contains a collection of Python scripts and modules that provide various reusable actions for different tasks. These actions include running bash commands, making API calls, generating prompts using OpenAI's GPT-3 model, publishing comments on GitHub issues, crawling folders, finding TODO comments in code, inserting content into text, and more. Each script or module represents a specific action and includes classes, methods, and data models for performing the task. The folder also includes a utility module for managing prompt context and a test module for testing the actions. Overall, these files provide a library of reusable actions that can be used in different Python programs.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/gh_actions_entrypoint.py)

📄 This file is the entry point for a GitHub Actions workflow.    
🔧 It sets up the necessary settings, services, and environment variables.    
🤖 The main purpose is to run the `MainService` class from the `autopr` package.    
🎯 It retrieves the necessary information from the environment variables.    
📝 The `get_event` method loads and extracts the event data for processing.    
🔑 The `get_platform_service` and `get_publish_service` methods create the necessary service instances.    
📂 The `get_repo_path` method retrieves the path to the GitHub workspace.    
📝 The `run` method of `MainService` is called to start the workflow.    
🚀 The file is executed when the script is run directly.  


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/log_config.py)

📝 This file configures logging and sets up a logger for use in the module.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/main.py)

📝 This file contains the implementation of the `MainService` class, which serves as the main entry point for running a series of triggers and workflows in an automated pull request workflow.  
🔧 It also defines the `Settings` class, which holds various configuration settings for the workflow.  
📂 The file imports necessary modules and classes from other files within the project.  
🔀 The `MainService` class initializes and configures various services and utilities required for the workflow, such as the commit service, action service, trigger service, and workflow service.  
🔄 The `run` method of the `MainService` class triggers the execution of the defined triggers and workflows.  
🔧 The file also contains several helper methods for retrieving repository information, event details, platform services, and branch names.  
🚀 The purpose of this file is to provide a centralized and organized implementation for orchestrating the automated pull request workflow.  
⚙️ It is intended to be used as part of a larger system or application that automates the process of creating and managing pull requests based on specified triggers and workflows.  
📖 The file serves as a starting point for understanding the overall structure and logic of the automated pull request workflow.  


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/models)

This folder contains files related to a codebase for automation and configuration management. The "artifacts.py" file defines Pydantic models for messages, threads, issues, and pull requests. The "config/" folder contains Python files for handling extra fields in models, executing actions and workflows, building workflow definitions and triggers, handling config and action variable transformations, and managing and rendering variables and parameters. The "events.py" file defines classes for different types of events in AutoPR. The "executable.py" file provides types and classes for context management and template rendering in a Python project.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/services)

This folder contains multiple Python files that implement various services and classes for managing and running actions, handling caching, working with Git repositories, making API calls to platforms like GitHub, publishing updates to pull requests, processing triggers, and executing workflows. These files provide functionality for different aspects of an automated pull request system, such as managing actions, caching data, handling commits and diffs, interacting with platforms, publishing updates, and executing workflows based on triggers. The files are well-documented and contain classes, methods, and helper functions that implement the necessary logic for each service.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.    
📁 The function takes two parameters: `config_dir` and `repo_path`.    
🔍 It searches for trigger configuration files in the specified directory and subdirectories.    
🔧 The trigger files can have either a `.yaml` or `.yml` extension.    
🔐 It loads the contents of each trigger file using the `yaml` library.    
🔁 If the file is empty or cannot be parsed, it is skipped.    
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.    
🔀 The function returns a list of all triggers extracted from the trigger files.    
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.  


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/8cf698d23fdb1a01845892b342672c06864b2fba/./autopr/workflows)

This folder contains a collection of Python scripts and YAML files that define workflows for various tasks. The scripts are focused on loading and managing workflows from YAML files, while the YAML files define specific workflows for tasks such as making API calls, generating README summaries, inserting content into files, managing TODO issues, and summarizing changes in pull requests. These files can be used as templates or starting points for automating and organizing tasks in a larger system.  

<!-- Living README Summary -->
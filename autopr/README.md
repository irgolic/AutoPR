

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files and folders related to an automated pull request workflow system. The `actions/` folder contains Python files that define various actions and utility functions for the system. The `gh_actions_entrypoint.py` file is the entry point for a GitHub Actions workflow. The `log_config.py` file configures logging for the system. The `main.py` file contains the implementation of the main service class and other necessary modules and classes. The `models/` folder contains files defining Pydantic models for the system. The `services/` folder contains files implementing various services and functionalities. The `triggers.py` file defines a function for retrieving and processing trigger configurations. The `workflows/` folder contains files for managing and organizing workflows in the system.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/actions)

This folder contains a collection of Python files that define various actions and utility functions for an autonomous agent system. Each file represents a specific action, such as running a bash command, making an API call, publishing a comment on GitHub, or searching for specific content in files. The files also include classes and functions for managing and transforming prompt context, as well as utility functions for reading and writing files. These actions and utilities can be used together to build a flexible and powerful autonomous agent system.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/gh_actions_entrypoint.py)

📄 This file is the entry point for a GitHub Actions workflow.    
🔧 It sets up the necessary settings, services, and environment variables.    
🤖 The main purpose is to run the `MainService` class from the `autopr` package.    
🎯 It retrieves the necessary information from the environment variables.    
📝 The `get_event` method loads and extracts the event data for processing.    
🔑 The `get_platform_service` and `get_publish_service` methods create the necessary service instances.    
📂 The `get_repo_path` method retrieves the path to the GitHub workspace.    
📝 The `run` method of `MainService` is called to start the workflow.    
🚀 The file is executed when the script is run directly.  


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/log_config.py)

📝 This file configures logging and sets up a logger for use in the module.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/main.py)

📝 This file contains the implementation of the `MainService` class, which serves as the main entry point for running a series of triggers and workflows in an automated pull request workflow.  
🔧 It also defines the `Settings` class, which holds various configuration settings for the workflow.  
📂 The file imports necessary modules and classes from other files within the project.  
🔀 The `MainService` class initializes and configures various services and utilities required for the workflow, such as the commit service, action service, trigger service, and workflow service.  
🔄 The `run` method of the `MainService` class triggers the execution of the defined triggers and workflows.  
🔧 The file also contains several helper methods for retrieving repository information, event details, platform services, and branch names.  
🚀 The purpose of this file is to provide a centralized and organized implementation for orchestrating the automated pull request workflow.  
⚙️ It is intended to be used as part of a larger system or application that automates the process of creating and managing pull requests based on specified triggers and workflows.  
📖 The file serves as a starting point for understanding the overall structure and logic of the automated pull request workflow.  


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/models)

This folder contains files related to a codebase for automation and configuration management. The "artifacts.py" file defines Pydantic models for messages, threads, issues, and pull requests. The "config/" folder contains Python files for handling extra fields in models, executing actions and workflows, building workflow definitions and triggers, handling config and action variable transformations, and managing and rendering variables and parameters. The "events.py" file defines classes for different types of events in AutoPR. The "executable.py" file provides types and classes for context management and template rendering in a Python project.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/services)

This folder contains several Python files that implement various services and functionalities for the autopr system. These files include classes for managing and running actions, caching data, creating and committing changes in a Git repository, getting and applying diffs, making API calls to platforms like GitHub, publishing updates to pull requests, handling triggers and executing workflows, and providing utility functions for formatting data. Each file has a specific purpose and provides the necessary methods and functionality for its respective service.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.    
📁 The function takes two parameters: `config_dir` and `repo_path`.    
🔍 It searches for trigger configuration files in the specified directory and subdirectories.    
🔧 The trigger files can have either a `.yaml` or `.yml` extension.    
🔐 It loads the contents of each trigger file using the `yaml` library.    
🔁 If the file is empty or cannot be parsed, it is skipped.    
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.    
🔀 The function returns a list of all triggers extracted from the trigger files.    
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.  


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/cde288186d52143cd526034ab0c0cce35e24583b/./autopr/workflows)

This folder contains a collection of files related to managing and organizing workflows. The main script, `__init__.py`, defines functions for loading and collecting workflows from YAML files. The other YAML files in the folder define specific workflows, such as making API calls, generating README summaries, inserting content into files, listing and publishing TODOs, and summarizing changes in pull requests. These files serve as templates and configurations for automating various tasks in a larger system.  

<!-- Living README Summary -->
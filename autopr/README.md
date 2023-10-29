

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a variety of Python files and folders related to an automation and AI system. The "actions" folder contains modules, classes, and scripts for importing, organizing, and executing different actions. The "models" folder provides data models for messages, threads, issues, and pull requests. The "services" folder contains various services for managing and automating actions within the system. The "triggers" file defines a function for retrieving and processing trigger configurations. The "workflows" folder contains scripts and YAML files that define workflows for various tasks. Overall, this folder provides reusable components and workflows for building automation and AI-related tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/__init__.py)

This file is empty.  


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions)

This folder contains a collection of Python files that serve different purposes. The files include modules for importing and organizing other Python files, base classes for defining actions in an autonomous agent system, scripts for running bash commands and making API calls, classes for generating prompts and searching for specific content, and utilities for managing prompt context in a chatbot application. There are also files for reading and writing file contents, publishing comments and issues on platforms, and finding and managing TODO tasks in code. Overall, this folder provides a variety of reusable components for building automation and AI-related tasks.  


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/gh_actions_entrypoint.py)

📝 This file is the entry point for a GitHub Actions workflow.  
🔧 It imports necessary modules and defines classes for the workflow.  
🚀 The purpose of this file is to configure and run the main service for GitHub Actions.  
⚙️ It sets up the necessary settings, platform service, and publish service for the workflow.  
🔑 It retrieves the required GitHub token and event information from environment variables.  
📂 The file also includes functions to get the repository path and load the event data.  
🔍 The event data is parsed and returned as an EventUnion object.  
📝 The file logs the start of the workflow and runs the main service using asyncio.  


### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/log_config.py)

📝 This file configures logging and sets up a logger for use in the module.  


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/main.py)

📝 This file contains the implementation of the `MainService` class, which is the main entry point for running the autopr application.   
🔧 It initializes various services and handles the execution of triggers and workflows based on the provided event.   
🔑 It also defines the `Settings` class for storing configuration options.   
📁 The file imports various modules and classes from other files in the project.   
⚙️ The `run` method is the main method that triggers the execution of the autopr application.  


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/models)

This folder contains files related to an automation system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config/` folder contains files for configuring actions, workflows, and context models. The `events.py` file defines classes for different types of events that can trigger the automation system. The `executable.py` file defines types and classes related to context variables, templates, and executables. Overall, this folder provides a foundation for building a flexible and extensible automation system.  


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services)

This folder contains various Python files that provide different services for managing and automating actions within the AutoPR system. These services include handling caching, managing commits and branches in a Git repository, applying and retrieving diffs, making API calls to a platform like GitHub, publishing updates to pull request descriptions, handling triggers and executing workflows, and providing utility functions for formatting and truncating nested Python objects for publishing purposes. Each file contains a class or classes with specific methods and functionality related to its respective service.  


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/triggers.py)

📄 This file defines a function called `get_all_triggers`.    
📁 The function takes two parameters: `config_dir` and `repo_path`.    
🔍 It searches for trigger configuration files in the specified directory and subdirectories.    
🔧 The trigger files can have either a `.yaml` or `.yml` extension.    
🔐 It loads the contents of each trigger file using the `yaml` library.    
🔁 If the file is empty or cannot be parsed, it is skipped.    
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.    
🔀 The function returns a list of all triggers extracted from the trigger files.    
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.  


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/workflows)

This folder contains a collection of Python scripts and YAML files that define workflows for various tasks. The scripts are used to collect and load workflows from YAML files, while the YAML files define specific actions and steps for tasks such as making API calls, generating README summaries, inserting content into files, managing TODOs in code repositories, and summarizing changes in pull requests. These workflows can be customized and automated to streamline and simplify these tasks.  

<!-- Living README Summary -->
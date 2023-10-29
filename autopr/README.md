

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a diverse set of functionalities and actions that can be used in various automation tasks. It includes files for defining base classes and actions for autonomous agent systems, as well as reusable components for running bash commands, generating prompts, reading and writing files, and searching for specific queries in directories. There are also files that implement specific actions, like publishing comments on GitHub issues or setting issue titles. Additionally, it contains code for managing prompt context in a chatbot application, as well as services and utilities for managing and automating tasks related to pull requests and Git repositories. The folder also includes files for defining triggers and workflows, and models for an AutoPR system. Overall, this folder provides a comprehensive set of tools for automating and managing tasks in a Git-based development workflow.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/__init__.py/)

This file is empty.


### [`actions/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/actions/)

This folder contains a collection of Python files that serve different purposes. Some files define base classes and actions for autonomous agent systems, such as performing tasks and making API calls. Other files provide reusable components for running bash commands, generating prompts, reading and writing files, and searching for specific queries in directories. There are also files that implement specific actions, like publishing comments on GitHub issues or setting issue titles. Additionally, there is a folder called "utils" that contains code for managing prompt context in a chatbot application. Overall, this folder represents a diverse set of functionalities and actions that can be used in various automation tasks.


### [`gh_actions_entrypoint.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/gh_actions_entrypoint.py/)

📝 This file is the entry point for a GitHub Actions workflow.
🔧 It imports necessary modules and defines classes for the workflow.
🚀 The purpose of this file is to configure and run the main service for GitHub Actions.
⚙️ It sets up the necessary settings, platform service, and publish service for the workflow.
🔑 It retrieves the required GitHub token and event information from environment variables.
📂 The file also includes functions to get the repository path and load the event data.
🔍 The event data is parsed and returned as an EventUnion object.
📝 The file logs the start of the workflow and runs the main service using asyncio.



### [`log_config.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/log_config.py/)

📝 This file configures logging and sets up a logger for use in the module.


### [`main.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/main.py/)

📝 This file contains the implementation of the `MainService` class, which is the main entry point for running the autopr application. 
🔧 It initializes various services and handles the execution of triggers and workflows based on the provided event. 
🔑 It also defines the `Settings` class for storing configuration options. 
📁 The file imports various modules and classes from other files in the project. 
⚙️ The `run` method is the main method that triggers the execution of the autopr application.


### [`models/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/models/)

This folder contains Python code and configuration files for an AutoPR system. The `artifacts.py` file defines data models for messages, threads, issues, and pull requests. The `config` folder contains files for handling extra fields, defining and executing actions and workflows, building workflow models and triggers, and converting between different representations of IO types. The `events.py` file defines classes for different types of events that can trigger the AutoPR system. The `executable.py` file contains types and classes related to context variables, templates, and executable actions.


### [`services/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/)

This folder contains a collection of Python files that implement various services and utilities for managing and automating tasks related to pull requests and Git repositories. These services include handling actions, caching data, managing commits and branches, applying and getting diffs, making API calls to platforms like GitHub, publishing updates to pull request descriptions, handling triggers and events, and executing workflows. The utilities include functions for formatting and truncating nested Python objects for publishing purposes. Overall, these files provide a comprehensive set of tools for automating and managing tasks in a Git-based development workflow.


### [`triggers.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/triggers.py/)

📄 This file defines a function called `get_all_triggers`.  
📁 The function takes two parameters: `config_dir` and `repo_path`.  
🔍 It searches for trigger configuration files in the specified directory and subdirectories.  
🔧 The trigger files can have either a `.yaml` or `.yml` extension.  
🔐 It loads the contents of each trigger file using the `yaml` library.  
🔁 If the file is empty or cannot be parsed, it is skipped.  
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.  
🔀 The function returns a list of all triggers extracted from the trigger files.  
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.


### [`workflows/`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/workflows/)

This folder contains a collection of files related to workflow configuration and execution. The main file, `__init__.py`, defines functions for collecting and loading workflows from YAML files in a specified folder and its subfolders. The other files contain specific workflow configurations, such as making API calls, generating README summaries, inserting content into files, and summarizing changes in pull requests. Each file serves a specific purpose and can be customized to automate various tasks.

<!-- Living README Summary -->
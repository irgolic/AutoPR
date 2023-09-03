

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and folders that collectively make up a system called AutoPR. The files define classes and actions for various tasks such as running commands, publishing comments on GitHub issues, committing and pushing changes to a remote repository, crawling folders and listing files, inserting content into strings, generating prompts using the OpenAI API, reading file contents, setting issue titles, and writing content into files. The folders contain additional code related to defining and transforming prompt contexts, managing and executing workflows, and handling triggers and configurations. Overall, these files and folders provide modular and reusable functionalities for building automated workflows or integrations.


### `__init__.py`

📄 This file appears to be empty.     
🤔 It is unclear what the purpose of this file is.     
🚫 No content or code is present in this file.     
🔍 There is no information to summarize.     
💡 Please check if any content is missing or if there was an error in the file.     
📝 This file may need to be filled with code or information.     
❌ Nothing to summarize at this time.     
📑 The purpose of this file is not apparent.     
🔒 No data or instructions are contained in this file.     
🔎 Review the file for any missing content or intended purpose.     


### `actions`

This folder contains a collection of Python files that serve different purposes. The files define classes and actions for various tasks such as running bash commands, publishing comments on GitHub issues, committing and pushing changes to a remote repository, crawling folders and listing files, inserting content into strings, generating prompts using the OpenAI API, reading file contents, setting issue titles, and writing content into files. The files make use of libraries like pydantic, asyncio, and openai, and demonstrate how to implement specific actions in automated processes. Additionally, there is a utils folder that contains code related to defining and transforming prompt contexts for auto PR generation.


### `gh_actions_entrypoint.py`

📝 This file is the entry point for a GitHub Actions workflow.
🔧 It imports necessary modules and defines classes for the workflow.
🚀 The purpose of this file is to configure and run the main service for GitHub Actions.
⚙️ It sets up the necessary settings, platform service, and publish service for the workflow.
🔑 It retrieves the required GitHub token and event information from environment variables.
📂 The file also includes functions to get the repository path and load the event data.
🔍 The event data is parsed and returned as an EventUnion object.
📝 The file logs the start of the workflow and runs the main service using asyncio.



### `log_config.py`

📝 This file configures logging and sets up a logger for use in the module.


### `main.py`

📝 This file contains the implementation of the `MainService` class and the `Settings` class. 
🔧 The `MainService` class is the main entry point for running the autopr workflow. 
🔀 It initializes various services such as the `PlatformService`, `PublishService`, `CommitService`, and `ActionService`. 
⚙️ It also handles the creation of branch names, triggering events, and running workflows. 
🔧 The `Settings` class provides default values for various configuration options.


### `models`

This folder contains Python files that define different aspects of a system called AutoPR. The "artifacts.py" file defines data models for messages, threads, issues, and pull requests. The "config" folder contains files related to configuration settings and handling of variables and parameters. The "events.py" file defines models for different types of events that can trigger AutoPR to run. The "executable.py" file contains types and classes related to context variables, templates, and executable actions.


### `services`

This folder contains several Python files that collectively provide various services and functionalities. These include managing and running actions in an automated process, providing a caching service, managing commits and branches in a Git repository, getting and applying diffs in a Git repository, making API calls to a platform (specifically GitHub) for tasks related to issues, pull requests, and comments, publishing updates to a pull request description, formatting and truncating nested Python objects for publishing purposes, and managing and executing workflows. These files are designed to be modular, extensible, and reusable for building automated workflows or integrations.


### `triggers.py`

📄 This file defines a function called `get_all_triggers`.  
📁 The function takes two parameters: `config_dir` and `repo_path`.  
🔍 It searches for trigger configuration files in the specified directory and subdirectories.  
🔧 The trigger files can have either a `.yaml` or `.yml` extension.  
🔐 It loads the contents of each trigger file using the `yaml` library.  
🔁 If the file is empty or cannot be parsed, it is skipped.  
📝 The contents of valid trigger files are converted into a list of `TopLevelTriggerConfig` objects.  
🔀 The function returns a list of all triggers extracted from the trigger files.  
📌 The purpose of this file is to provide a convenient way to retrieve and process trigger configurations.


### `workflows`

This folder contains Python scripts and YAML files for loading and collecting workflows. The `__init__.py` file defines functions for loading workflows from YAML files in a folder and its subfolders, and the `get_all_workflows` function is the entry point. The `autogenerate_readmes.yaml` file contains workflows for summarizing files and folders in a directory and generating README summaries. The `insert_into_readme.yaml` file defines a task for inserting content into a file with optional tag-based delimiters. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request.

<!-- Living README Summary -->
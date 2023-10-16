

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files that provide various services and functionalities. The files include implementations for managing and running actions in an automated process, providing a caching service, managing commits and branches in a Git repository, handling diffs in a repository, interacting with the GitHub platform, managing and updating pull request descriptions, handling triggers and executing workflows, and formatting and truncating nested Python objects for publishing purposes. These files can be used together to create an automated pull request workflow or individually for specific functionalities.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/__init__.py/)

This file is empty.


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/action_service.py/)

💡 This file contains the implementation of the `ActionService` class, which is responsible for managing and running actions in an automated process. It provides methods for finding, instantiating, and running actions, as well as handling inputs and outputs. The file also imports various modules and defines some helper classes and functions.


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/cache_service.py/)

📁 The file contains a class called `CacheService` and a subclass called `ShelveCacheService`.
📦 The purpose of the file is to provide a caching service using the `shelve` module.
🔒 The `CacheService` class defines methods for storing and retrieving data from the cache.
🔑 The `ShelveCacheService` class extends `CacheService` and implements the caching functionality using the `shelve` module.
📝 The `store` method stores a key-value pair in the cache.
🔍 The `retrieve` method retrieves a value from the cache based on a given key.
🗂️ The cache is organized into namespaces, which can be specified or default to a value provided during initialization.
📂 The cache is stored in a folder specified by the `config_dir` parameter during initialization.
🚧 The cache folder is created if it doesn't exist.
❌ If the `store` or `retrieve` methods are called without specifying a namespace, the default namespace is used.


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/commit_service.py/)

📝 The file contains a class called `CommitService`.
🔧 The `CommitService` class provides methods for creating branches, committing changes, and pushing them to a Git repository.
🌱 It ensures that there is always a commit on the branch.
📂 The class takes in parameters such as the repository, repository path, branch name, and base branch name.
🔀 The `overwrite_new_branch` method creates a new branch by checking out the base branch, pulling the latest changes, and then creating a new branch with an empty commit.
🔄 The `ensure_branch_exists` method checks if a branch already exists and either checks it out and pulls the latest changes or creates a new branch.
📝 The `commit` method adds and commits changes, and can also push the branch to the remote repository.
📚 The class uses the `git` module for interacting with Git commands.
🔍 The class logs debug and info messages using a logger.
👥 The purpose of this file is to provide a service for managing commits and branches in a Git repository.


### [`diff_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/diff_service.py/)

📄 This file contains the implementation of a `DiffService` class and its subclasses `GitApplyService` and `PatchService`.  
🔀 The purpose of these classes is to provide functionality for getting and applying diffs in a Git repository.  
🔧 The `DiffService` class has methods for getting and applying diffs, while the subclasses provide specific implementations for applying diffs using `git apply` and `patch` commands.  
📝 Diffs are represented as `DiffStr`, which is a type alias for a string.  
📁 The `DiffService` class takes a `Repo` object as a parameter, which represents a Git repository.  
📝 The `apply_diff` method in the `DiffService` class is not implemented and raises a `NotImplementedError`.  
⚙️ The `get_diff` method in the `DiffService` class retrieves the diff for the specified file paths or for all files in the repository if no file paths are provided.  
📝 The `apply_diff` method in the `GitApplyService` subclass applies the diff using the `git apply` command.  
📝 The `apply_diff` method in the `PatchService` subclass applies the diff using the `patch` command.  
🔧 The `apply_diff` methods in both subclasses have an optional `check` parameter which, when set to `True`, performs a dry run of the diff application.


### [`platform_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/platform_service.py/)

📝 This file contains the implementation of a platform service for making API calls to the GitHub platform.
📡 It includes methods for publishing comments, setting titles, creating and merging pull requests, updating pull request bodies and titles, and handling events.
🔒 The GitHubPlatformService class extends the PlatformService class and provides the specific implementation for interacting with the GitHub API.
⚙️ The DummyPlatformService class is a dummy implementation of the PlatformService for testing purposes.
🔗 The PlatformService class defines the common interface and abstract methods that need to be implemented by platform-specific service classes.
📚 It also includes models for representing issues, pull requests, events, and messages.
📁 The autopr.log_config module is imported to configure logging.
🔗 The typing module is imported to define type hints for the methods.
🚫 The NotImplementedError is raised for the abstract methods that need to be implemented by the subclasses.
💡 The purpose of this file is to provide a reusable and extensible service for interacting with the GitHub platform in an automated pull request workflow.


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/publish_service.py/)

📝 This file defines the `PublishService` class and its subclasses `GitHubPublishService` and `DummyPublishService`.
📝 The `PublishService` class provides methods for publishing updates to a pull request description.
📝 It allows for creating sections, updating section titles, and publishing text and code blocks.
📝 The `GitHubPublishService` subclass adds functionality specific to publishing on GitHub, such as setting draft status and adding a shield to the PR description.
📝 The `DummyPublishService` subclass is a dummy implementation used for testing or as a placeholder.
📝 The purpose of this file is to provide a service for managing and updating the description of a pull request.
📝 It is used to track and display progress, errors, and updates related to the pull request.
📝 The file also includes the `CodeBlock` and `UpdateSection` models used by the `PublishService` class.
📝 The `CodeBlock` model represents a block of code to be shown in the pull request description.
📝 The `UpdateSection` model represents a section of the pull request description, used to keep track of updates and state.
📝 The `PublishService` class and its subclasses are part of a larger system for automating pull request management and updates.


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/trigger_service.py/)

📄 This file contains the implementation of the `TriggerService` class. 
🔫 The purpose of this class is to handle triggers and execute workflows based on events. 
🚀 It receives events, matches them with triggers, and executes the associated workflows. 
💥 It also handles publishing and logging of trigger and workflow execution details. 
🔁 The `trigger_event` method is the main entry point, which triggers the execution of workflows based on the provided event. 
📝 The `handle_trigger` method executes a single trigger and workflow, handling parameters and publishing the execution details. 
🔧 Other helper methods are provided to gather triggers and contexts for an event, build coroutines for triggers, and get the name of an executable. 
📚 The class depends on other services such as `PublishService` and `WorkflowService` to perform its tasks. 
🔍 The class is initialized with a list of triggers, a publish service, and a workflow service. 
📢 Triggers are printed when the class is initialized.


### [`utils.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/utils.py/)

📄 This file contains a set of utility functions for formatting and truncating nested Python objects for publishing purposes.
🔍 The main function, `format_for_publishing`, takes an object and converts it to a JSON string, while also truncating any long strings and excluding certain keys.
🔄 The `truncate_strings` function is used to truncate strings within the object to a specified length, appending "(truncated)" to indicate truncation.
🔀 The `nested_to_dict` function recursively converts nested objects (dicts, lists, and pydantic models) into dictionaries.
📝 The `format_for_publishing` function uses `nested_to_dict` to convert the input object into a dictionary, then excludes certain keys and truncates strings before converting the dictionary to a JSON string.
🔑 The purpose of these functions is to provide a convenient way to format and prepare nested Python objects for publishing or displaying purposes.
🧩 These utility functions can be used in various scenarios where it is necessary to format and truncate nested objects, such as when displaying data in a web application or logging structured information.
📝 The file utilizes the `pydantic` library for working with structured data and type validation.
📦 The file does not contain any specific usage examples or tests, but it provides reusable functions that can be imported and used in other Python scripts or modules.
🔎 Overall, this file serves as a helpful set of utility functions for formatting and truncating nested Python objects for publishing purposes, providing flexibility and convenience in working with structured data.


### [`workflow_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/workflow_service.py/)

📝 This file contains the implementation of the `WorkflowService` class, which is responsible for executing workflows and actions based on their IDs. It provides methods for invoking workflows, running actions, and handling inputs and outputs.

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various Python files that serve different purposes. Some files provide services for managing actions, caching data, handling commits and branches in a Git repository, and interacting with a platform's API. Other files provide utility functions for formatting and truncating nested Python objects and publishing updates to a pull request description. There are also files related to triggers and workflows, as well as a file containing empty initialization code. Each file has a specific role in the overall functionality of the system.


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

📝 This file contains a Python module that defines classes for interacting with a platform (e.g., GitHub) through its API.
📚 The main class is `PlatformService`, which provides methods for performing various actions on the platform, such as creating pull requests, merging pull requests, and updating issues.
🔎 The module also includes a subclass called `GitHubPlatformService`, which specifically implements the functionality for interacting with the GitHub platform.
🔒 The `GitHubPlatformService` class requires a token for authentication with the GitHub API.
📥 There is also a `DummyPlatformService` class, which is a placeholder implementation of the `PlatformService` class for testing purposes.
🚧 Some methods in the classes are marked as `NotImplementedError`, indicating that they need to be implemented in a subclass.
🌟 The module includes additional utility methods for parsing events from the platform and extracting information from JSON responses.
🔌 The module imports various dependencies, such as `asyncio`, `aiohttp`, and `requests`, for making HTTP requests and handling asynchronous operations.
📄 The module includes type hints for function parameters and return values.
💡 Overall, this module provides a convenient interface for interacting with a platform's API and performing common actions on the platform, such as creating pull requests and updating issues.


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/publish_service.py/)

📋 This file contains the implementation of a PublishService class and its subclasses, GitHubPublishService and DummyPublishService. These classes are used to publish updates and progress to a pull request description on a platform (such as GitHub). The PublishService class provides methods for updating the pull request description, publishing text updates and code blocks, starting and ending sections, and merging the pull request. The GitHubPublishService subclass adds additional functionality specific to GitHub, such as adding a shield linking to the action logs and a "Fixes #{issue_number}" link. The DummyPublishService subclass is a dummy implementation used for testing purposes.


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/trigger_service.py/)

📝 This file contains the implementation of the `TriggerService` class.
🔄 The `TriggerService` class handles triggers and their associated actions in a workflow.
🔀 Triggers are matched to events and their corresponding contexts.
📝 The `_get_name_for_executable` method returns the name of the executable associated with a trigger.
🔀 The `_get_triggers_and_contexts_for_event` method gathers triggers that match a given event.
🔄 The `_get_trigger_coros_for_event` method builds coroutines for each trigger.
📝 The `trigger_event` method triggers the execution of actions based on an event.
🔄 The `handle_trigger` method executes a trigger's associated action.
📝 The file also contains various utility methods and imports.


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
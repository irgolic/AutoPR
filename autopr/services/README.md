

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files that provide various services and utilities for managing and automating tasks within the AutoPR system. The files include implementations for services such as managing actions, caching data, handling commits and branches in a Git repository, applying and getting diffs, making API calls to a platform like GitHub, publishing updates to a pull request, handling triggers and executing workflows, and formatting and truncating nested Python objects. These files are designed to work together to provide a comprehensive set of functionality for automating and managing tasks within the AutoPR system.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/__init__.py/)

This file is empty.


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/action_service.py/)

💡 This file contains the implementation of the `ActionService` class, which is responsible for managing and running actions within the AutoPR system. It provides methods for finding, instantiating, and running actions, as well as handling inputs and outputs.


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/cache_service.py/)

📁 The file contains a Python class called `CacheService` and its implementation called `ShelveCacheService`.
🔒 The purpose of the file is to provide a caching service that stores and retrieves key-value pairs.
🗄️ The caching service uses the `shelve` module to store data in a persistent file-based database.
🔑 The `store` method is used to store a key-value pair in the cache.
🔍 The `retrieve` method is used to retrieve the value associated with a given key from the cache.
📂 The cache can be organized into different namespaces, allowing for separation of data.
📁 The default namespace is based on an `action_id` provided during initialization.
📂 The cache is stored in a directory specified by `cache_dir`.
🔑 The `store` and `retrieve` methods handle key preparation and loading of the cache file for the specified namespace.
⚠️ The class raises a `NotImplementedError` for the `store` and `retrieve` methods, indicating that they need to be implemented in a subclass.


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/commit_service.py/)

📝 This file contains a class called `CommitService` which is responsible for managing branches, committing changes, and pushing changes to a Git repository.
📁 It imports necessary modules and defines a type `CHANGES_STATUS` for representing different states of changes on a branch.
🔧 The `CommitService` class has methods for creating a new branch, ensuring that a branch exists, committing changes, and checking the status of changes.
🗂️ The `overwrite_new_branch` method creates a new branch based on a base branch and makes an empty commit on it.
🔄 The `ensure_branch_exists` method checks if a branch exists and pulls the latest changes if it does. If the branch doesn't exist, it creates a new branch based on a remote branch.
💾 The `commit` method adds and commits changes to the branch, with an option to push the changes to the remote repository.
🔍 The `get_changes_status` method returns the status of changes on the branch, indicating whether there are no changes, only cached changes, or modified changes.
🔒 The class uses a logger for logging debug and info messages.
📝 The purpose of this file is to provide a service for managing commits and branches in a Git repository, ensuring that there is always a commit on the branch.


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

📝 The purpose of this file is to define classes for making API calls to a platform (e.g., GitHub) and provide methods for interacting with pull requests and issues.
📌 The `PlatformService` class is an abstract base class that defines the common interface for making API calls to the platform.
📌 The `GitHubPlatformService` class is a concrete implementation of the `PlatformService` class specifically for interacting with GitHub.
📌 The `DummyPlatformService` class is a dummy implementation of the `PlatformService` class that does not actually make any API calls.
📌 The `PlatformService` class defines methods for publishing comments, setting the title of a pull request, getting a list of issues, finding existing pull requests, creating pull requests, merging pull requests, closing pull requests, updating the body and title of pull requests, updating comments, and parsing platform events.
📌 The `GitHubPlatformService` class implements the methods defined in the `PlatformService` class for interacting with GitHub's API.
📌 The `DummyPlatformService` class provides empty implementations of the methods defined in the `PlatformService` class.
📌 The `GitHubPlatformService` class uses the `aiohttp` library for making asynchronous HTTP requests to the GitHub API.
📌 The `GitHubPlatformService` class also uses the `requests` library for making synchronous HTTP requests to the GitHub API in some cases.
📌 The `GitHubPlatformService` class includes methods for setting the draft status of a pull request, updating the body and title of an issue, and getting the URL of a file in the repository.


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/publish_service.py/)

📄 This file contains the implementation of a service for publishing updates to a pull request description. 

🔹 The service allows for creating sections and updating their titles.
🔹 It supports publishing simple textual updates and code blocks in the pull request description.
🔹 The service can set the title and body of the pull request.
🔹 It can merge or close the pull request.
🔹 The service can create child instances to manage updates within specific sections.
🔹 It provides methods for updating the pull request description and finalizing the pull request.
🔹 The service supports publishing comments on the pull request.
🔹 There are subclasses for publishing to GitHub and a dummy implementation for testing.
🔹 The file also includes model classes for CodeBlock and UpdateSection.


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/trigger_service.py/)

📚 This file contains the implementation of the `TriggerService` class.  
🔗 The `TriggerService` class is responsible for handling triggers and executing workflows based on events.  
🔁 It has methods for getting the name of an executable, getting triggers and contexts for an event, and handling trigger events.  
💡 The `finalize_trigger` method is used to handle the finalization of a trigger, including merging or closing a pull request.  
📣 The `handle_trigger` method is responsible for executing a trigger and publishing the trigger and context information.  
🔧 The class relies on other services such as `PublishService`, `WorkflowService`, and `CommitService` for its functionality.  
🔗 Triggers are defined in a list and passed to the `TriggerService` constructor.  
🚀 The `trigger_event` method is called to trigger the execution of workflows based on an event.  
📝 The file also includes some helper methods and logging functionality.


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

📝 This file contains the implementation of the WorkflowService class, which is responsible for executing workflows. Workflows are defined as a series of steps, which can include actions, nested workflows, and iterative workflows. The class provides methods for executing workflows by their ID, invoking workflows and iterative workflows, and validating inputs and outputs. It also includes helper methods for preparing workflow inputs and publishing execution logs.

<!-- Living README Summary -->
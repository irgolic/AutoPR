

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various Python files that serve different purposes. Some files provide services for managing actions, caching, commits, diffs, platforms, publishing updates, and workflows. There are also utility functions for formatting and truncating nested objects. These files are part of the AutoPR project and are used for automating pull request actions and managing related tasks.


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

📝 This file contains the implementation of two classes: `PlatformService` and `GitHubPlatformService`.
📦 The `PlatformService` class is a base class for making API calls to a platform, such as GitHub.
🔍 It provides methods for interacting with issues, pull requests, comments, and files in a repository.
🚀 The `GitHubPlatformService` class is a subclass of `PlatformService` specifically for interacting with the GitHub platform.
🔑 It requires a token for authentication and provides additional methods for creating and updating pull requests, comments, and issues on GitHub.
❌ There is also a `DummyPlatformService` class provided, which is a dummy implementation of `PlatformService` for testing purposes.
🧩 The file also includes some helper functions and data models used by the classes.
📚 The classes use the `aiohttp` library for making asynchronous HTTP requests to the GitHub API.
🔒 The `GitHubPlatformService` class uses the GitHub API v3 and, when available, the GitHub GraphQL API for certain operations.
📖 The file includes type hints and docstrings for the methods and classes to provide usage information and improve code readability.


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/services/publish_service.py/)

📝 This file contains the implementation of a service called "PublishService" and its subclasses "GitHubPublishService" and "DummyPublishService". 
📄 The file defines several classes and models related to publishing updates to a pull request description. 
🔧 The "PublishService" class provides methods for controlling update sections and publishing updates to the current section. 
📝 The "CodeBlock" model represents a block of text to be shown as a code block in the pull request description. 
📝 The "UpdateSection" model represents a section of the pull request description, used to keep state while publishing updates. 
🔧 The "PublishService" class also provides methods for starting a new section, ending the current section, and updating the title of the current section. 
📄 The "GitHubPublishService" class is a subclass of "PublishService" specifically designed for publishing updates to GitHub pull requests. 
📄 The "DummyPublishService" class is a subclass of "PublishService" that serves as a dummy implementation for testing purposes. 
🔧 The file also includes some helper methods and attributes for handling errors and building the PR body. 
🔧 The purpose of this file is to provide a convenient way to publish updates and manage the pull request description in an automated manner.


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

📝 This file contains the implementation of the WorkflowService class, which is responsible for managing and executing workflows. 
🌊 It handles triggers, events, and the execution of actions and workflows. 
🔧 It also provides methods for validating inputs and outputs of workflows. 
🚀 The WorkflowService class is used in the AutoPR project for automating pull request actions.

<!-- Living README Summary -->
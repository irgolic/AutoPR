

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various Python files that provide different services for managing and automating actions within the AutoPR system. These services include handling caching, managing commits and branches in a Git repository, applying and retrieving diffs, making API calls to a platform like GitHub, publishing updates to pull request descriptions, handling triggers and executing workflows, and providing utility functions for formatting and truncating nested Python objects for publishing purposes. Each file contains a class or classes with specific methods and functionality related to its respective service.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/__init__.py)

This file is empty.  


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/action_service.py)

💡 This file contains the implementation of the `ActionService` class, which is responsible for managing and running actions within the AutoPR system. It provides methods for finding, instantiating, and running actions, as well as handling inputs and outputs.  


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/cache_service.py)

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


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/commit_service.py)

📝 This file contains a class called `CommitService` which is responsible for managing branches, committing changes, and pushing changes to a Git repository.  
📁 It imports necessary modules and defines a type `CHANGES_STATUS` for representing different states of changes on a branch.  
🔧 The `CommitService` class has methods for creating a new branch, ensuring that a branch exists, committing changes, and checking the status of changes.  
🗂️ The `overwrite_new_branch` method creates a new branch based on a base branch and makes an empty commit on it.  
🔄 The `ensure_branch_exists` method checks if a branch exists and pulls the latest changes if it does. If the branch doesn't exist, it creates a new branch based on a remote branch.  
💾 The `commit` method adds and commits changes to the branch, with an option to push the changes to the remote repository.  
🔍 The `get_changes_status` method returns the status of changes on the branch, indicating whether there are no changes, only cached changes, or modified changes.  
🔒 The class uses a logger for logging debug and info messages.  
📝 The purpose of this file is to provide a service for managing commits and branches in a Git repository, ensuring that there is always a commit on the branch.  


### [`diff_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/diff_service.py)

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


### [`platform_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/platform_service.py)

📝 The file contains the implementation of a platform service for making API calls to a platform like GitHub.  
📚 It includes methods for performing various actions such as publishing comments, creating and merging pull requests, and updating issues.  
🔒 The `GitHubPlatformService` class extends the `PlatformService` class and provides specific functionality for interacting with the GitHub platform.  
🔒 It includes methods for finding existing pull requests, creating pull requests, merging pull requests, updating pull request bodies, and more.  
🌐 The `DummyPlatformService` class is a dummy implementation of the platform service for testing purposes.  
🌐 It provides empty implementations of the methods and can be used as a placeholder or for testing without making actual API calls.  
🔧 The file also includes helper methods for logging and handling API requests.  
🔧 There are methods for parsing events from the platform and extracting relevant information such as pull requests and issues.  
🔧 The file includes a `PRBodySentinel` class used as a sentinel value for representing pull request bodies.  
🔧 There are methods for getting the URL of a file in the repository and performing operations on issues such as creating, updating, and closing them.  


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/publish_service.py)

📝 This file contains the implementation of a service for publishing updates to a pull request description.  
📋 The service allows for controlling update sections and publishing updates to the current section.  
💻 It includes functionality for publishing simple text updates and code blocks.  
🔗 The service can create child instances to manage updates in nested sections.  
🚀 It provides methods for merging and closing the pull request.  
📈 The service can update the pull request description with the current progress.  
📖 It supports both concise and detailed progress updates.  
🔍 The service can search for an existing pull request and overwrite its description if necessary.  
🐙 The file includes the implementation of a GitHub-specific version of the service.  
📄 There is also a dummy version of the service for testing purposes.  


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/trigger_service.py)

📝 This file contains the implementation of the `TriggerService` class.   
🔗 The purpose of this class is to handle triggers and execute workflows based on events.   
🔄 Triggers are defined as instances of the `Trigger` class.   
🚀 The `trigger_event` method is used to trigger the execution of workflows based on an event.   
🔍 The `_get_triggers_and_contexts_for_event` method is used to gather all triggers that match the event.   
🔗 The `_get_trigger_coros_for_event` method builds coroutines for each trigger based on the event.   
🔧 The `handle_trigger` method is responsible for executing the workflow associated with a trigger.   
✅ The `finalize_trigger` method is called after the execution of all triggers and handles the finalization of the trigger process.   
📝 The file also includes helper methods for getting the ID and name of an executable.  


### [`utils.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/utils.py)

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


### [`workflow_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/services/workflow_service.py)

📝 This file defines a class called `WorkflowService` that provides methods for executing workflows and actions based on their IDs. It also handles the preparation of inputs and outputs for workflows and actions. The class takes in a `TopLevelWorkflowConfig`, an `ActionService`, and a `PublishService` as parameters.  

<!-- Living README Summary -->
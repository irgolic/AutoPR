

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various Python files that implement different services and classes for managing and running actions in an automated pull request (PR) workflow. These services include the ActionService, CacheService, CommitService, DiffService, PlatformService, PublishService, TriggerService, and WorkflowService. Each service has its own specific purpose, such as handling actions, caching data, managing commits, applying and getting diffs, interacting with the GitHub platform, publishing updates to PRs, handling triggers and executing workflows, and providing utility functions for formatting and truncating data. The files also include subclasses and helper functions to support the main functionality of each service.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/__init__.py)

This file is empty.  


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/action_service.py)

💼 This file contains the implementation of the `ActionService` class, which is responsible for managing and running actions in an automated PR workflow.  
💧 The `ActionService` class provides methods for finding, instantiating, and running actions based on their configurations.  
💧 It can handle both regular actions and iterative actions that run multiple times.  
💧 The class also handles input and output processing, including validation and formatting.  
💾 It uses various services such as `PublishService`, `PlatformService`, `CommitService`, and `CacheService` to perform its tasks.  
📝 The file also includes some helper functions for resolving input values and formatting outputs.  
🔧 The `ActionService` class is initialized with a `Repo` object, a cache directory, and other optional parameters.  
👥 The `actions` attribute of the class holds a dictionary of all available actions, loaded from the `autopr/actions` directory.  
🚀 The main methods of the class are `run_action()` and `run_action_iteratively()`, which execute the specified actions and handle the publishing of inputs, outputs, and errors.  
⚠️ If an action fails to run, an error message is displayed and the exception is raised.  


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/cache_service.py)

📁 The file contains a class called `CacheService` and its subclass `ShelveCacheService`.    
📝 The purpose of the file is to provide a caching service using the `shelve` module.    
🔒 The `ShelveCacheService` class allows storing and retrieving key-value pairs in a cache directory.    
💾 The cache directory is created if it doesn't exist.    
🔑 The cache can be organized using namespaces.    
🚀 The `store` method stores a key-value pair in the cache.    
🔍 The `retrieve` method retrieves the value associated with a key from the cache.    
❗️ The methods can accept an optional namespace parameter to specify a specific cache namespace.    
📂 The cache data is stored in separate files within the cache directory.    
🔒 The cache files are opened and closed using the `shelve` module.  


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/commit_service.py)

📝 The file contains a class called `CommitService`.  
🔀 The purpose of the class is to handle creating branches, committing changes, and pushing them to a Git repository.  
🔄 It ensures that there is always a commit on the branch.  
📚 The class has several methods such as `overwrite_new_branch`, `ensure_branch_exists`, `unstaged_changes_exist`, `commit`, and `get_changes_status`.  
📝 The `overwrite_new_branch` method deletes an existing branch, creates a new branch based on a base branch, and checks it out.  
📝 The `ensure_branch_exists` method checks if a branch already exists, and if not, creates a new branch based on a remote branch.  
🔍 The `unstaged_changes_exist` method checks if there are any unstaged changes in the repository.  
📝 The `commit` method adds and commits changes to the branch, and optionally pushes the branch to the remote repository.  
📝 The `get_changes_status` method returns the status of the changes on the branch (no changes, cache only, or modified).  


### [`diff_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/diff_service.py)

📝 The file contains a class called `DiffService` which is a service for getting and applying diffs.  
📝 Diffs are represented as `DiffStr`, which is an alias for `str`.  
📝 The `DiffService` class has methods for applying a diff and getting a diff.  
📝 There are two subclasses of `DiffService` called `GitApplyService` and `PatchService`.  
📝 The `GitApplyService` class overrides the `apply_diff` method to apply the diff using the `git apply` command.  
📝 The `PatchService` class overrides the `apply_diff` method to apply the diff using the `patch` command.  
📝 Both subclasses use temporary files to store the diff before applying it.  
📝 The `GitApplyService` class allows an optional `check` parameter to perform a dry run of applying the diff.  
📝 The `PatchService` class also allows an optional `check` parameter to perform a dry run of applying the diff.  
📝 The file includes a logger for debugging purposes.  


### [`platform_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/platform_service.py)

📄 This file contains two classes: `PlatformService` and `GitHubPlatformService`.  
🔧 `PlatformService` is a base class for making API calls to a platform (e.g., GitHub).  
🔀 `GitHubPlatformService` is a subclass of `PlatformService` specifically for publishing pull requests to GitHub.  
🔐 It requires a token for authentication.  
📝 It provides methods for publishing comments, creating and merging pull requests, updating pull request titles and bodies, and more.  
🔗 It also has methods for creating and updating issues on GitHub.  
📂 The `DummyPlatformService` class is a dummy implementation of `PlatformService` for testing purposes.  
🧠 The file also includes some helper methods and classes related to parsing events and working with GitHub APIs.  
🚫 The methods in the `PlatformService` class raise a `NotImplementedError` to indicate that they need to be implemented in subclasses.  
🌐 The purpose of this file is to provide a service for interacting with the GitHub platform, including creating and managing pull requests and issues.  


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/publish_service.py)

💡 This file contains the implementation of a service for publishing updates to a pull request description. It includes classes like `CodeBlock` and `UpdateSection` to represent different elements in the description. The main class is `PublishService`, which provides methods for updating and finalizing the pull request description. There are also subclasses `GitHubPublishService` and `DummyPublishService` for specific platforms.  


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/trigger_service.py)

📝 This file contains the implementation of a TriggerService class.   
🔗 The TriggerService class is responsible for handling triggers and executing workflows based on events.   
🔀 Triggers are defined in a list and matched against incoming events to determine which workflows to run.   
📥 The TriggerService takes in instances of PublishService, WorkflowService, and CommitService as dependencies.   
🔁 The TriggerService has methods for getting the ID and name of an executable, getting triggers and contexts for an event, and handling triggers.   
📣 The handle_trigger method executes a workflow and publishes the trigger, starting context, and final context.   
🔧 The finalize_trigger method handles the finalization of a trigger, including committing changes, merging PRs, and closing PRs.   
🏁 The trigger_event method is the entry point for triggering events and executing workflows based on those events.   
💡 The file also includes some helper methods and imports from external modules.  


### [`utils.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/utils.py)

💡 This file contains functions for formatting and truncating data for publishing.   
💡 The `truncate_strings` function truncates strings to a specified length and adds an ellipsis if necessary.   
💡 The `nested_to_dict` function converts nested objects (such as dictionaries and lists) to dictionaries.   
💡 The `format_for_publishing` function formats an object for publishing by converting it to a dictionary, truncating strings, and removing certain keys.   
💡 The file uses the `pydantic` library for working with data models.   
💡 The functions are designed to be used together to prepare data for display or publication.  


### [`workflow_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/services/workflow_service.py)

📄 This file contains the implementation of a WorkflowService class.   
🌊 The WorkflowService class is responsible for executing workflows and actions based on their IDs.   
🔀 It can handle both single invocations and iterative invocations of workflows.   
💡 The class provides methods for preparing the workflow context, validating inputs and outputs, and executing the workflow steps.   
🚀 It uses an ActionService and a PublishService for running actions and publishing results.   
✅ The class also includes methods for retrieving executable objects by their IDs and handling errors.   
🔧 It utilizes other modules and classes from the autopr package for configuration and logging.   
📝 The file also contains import statements and type annotations for the defined classes and functions.   
📚 The code is well-documented with comments explaining the purpose and functionality of each method.   
🔒 The strict parameter in the class constructor determines whether missing inputs and outputs should raise errors or warnings.  

<!-- Living README Summary -->
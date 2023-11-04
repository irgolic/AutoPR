

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains several Python files that make up a set of services for managing and running actions in an automated pull request workflow. These services handle tasks such as caching, committing changes, applying diffs, interacting with the GitHub platform, and publishing updates to pull request descriptions. There is also a service for executing workflows and handling triggers based on events. Additionally, there are some utility functions for formatting and truncating data for publishing. The code is well-documented and includes import statements and type annotations.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/__init__.py)

This file is empty.  


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/action_service.py)

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


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/cache_service.py)

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


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/commit_service.py)

📝 This file contains a class called `CommitService` that provides methods for managing branches, committing changes, and pushing to a Git repository.  
📝 The `CommitService` ensures that there is always a commit on the branch.  
📝 The `overwrite_new_branch` method creates a new branch based on a base branch, deletes the existing branch if it already exists, and creates an empty commit on the new branch.  
📝 The `ensure_branch_exists` method checks if a branch exists, and if it does, checks out and pulls the latest changes. If the branch does not exist, it creates a new branch based on a base branch.  
📝 The `unstaged_changes_exist` method checks if there are any unstaged changes in the repository.  
📝 The `commit` method adds and commits changes to the repository, and optionally pushes the branch to the remote repository.  
📝 The `get_changes_status` method returns the status of the changes on the branch, indicating whether there are no changes, only cache changes, or modified changes.  


### [`diff_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/diff_service.py)

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


### [`platform_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/platform_service.py)

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


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/publish_service.py)

💡 This file contains the implementation of a service for publishing updates to a pull request description. It includes classes like `CodeBlock` and `UpdateSection` to represent different elements in the description. The main class is `PublishService`, which provides methods for updating and finalizing the pull request description. There are also subclasses `GitHubPublishService` and `DummyPublishService` for specific platforms.  


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/trigger_service.py)

📝 This file contains the implementation of the `TriggerService` class.    
🔗 The `TriggerService` class is responsible for handling triggers and executing workflows based on events.    
📋 Triggers are defined as instances of the `Trigger` class.    
🖥️ The `TriggerService` class has methods for getting the ID and name of an executable, getting triggers and contexts for an event, and handling triggers.    
⚙️ The `trigger_event` method is called to trigger a workflow based on an event.    
✅ The `finalize_trigger` method is called to finalize the trigger and perform actions like committing changes and merging the PR.    
🔁 The `handle_trigger` method is called to handle a specific trigger and execute the associated workflow.    
📣 The `publish_service` is used to publish information and code blocks during the trigger and workflow execution.    
🔧 Other services like `PublishService`, `WorkflowService`, and `CommitService` are injected into the `TriggerService` class.  


### [`utils.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/utils.py)

💡 This file contains functions for formatting and truncating data for publishing.   
💡 The `truncate_strings` function truncates strings to a specified length and adds an ellipsis if necessary.   
💡 The `nested_to_dict` function converts nested objects (such as dictionaries and lists) to dictionaries.   
💡 The `format_for_publishing` function formats an object for publishing by converting it to a dictionary, truncating strings, and removing certain keys.   
💡 The file uses the `pydantic` library for working with data models.   
💡 The functions are designed to be used together to prepare data for display or publication.  


### [`workflow_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr/services/workflow_service.py)

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
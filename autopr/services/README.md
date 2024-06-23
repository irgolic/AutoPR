

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files that implement various services and classes for managing and running actions in an automated PR workflow. These services include the `ActionService` for finding, instantiating, and running actions, the `CacheService` for storing and retrieving key-value pairs in a cache directory, the `CommitService` for handling Git-related operations, the `DiffService` for getting and applying diffs, the `PlatformService` for interacting with the GitHub platform, the `PublishService` for publishing updates to a pull request description, the `TriggerService` for handling triggers for events, the `Utils` module for formatting and truncating data, and the `WorkflowService` for executing workflows and actions based on their IDs.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/__init__.py)

This file is empty.  


### [`action_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/action_service.py)

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


### [`cache_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/cache_service.py)

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


### [`commit_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/commit_service.py)

📝 This file contains a class called `CommitService` which provides methods for creating branches, committing changes, and pushing them to a Git repository.  
🚀 The purpose of this file is to handle the Git-related operations necessary for managing commits and branches.  
🌿 The `CommitService` class ensures that there is always a commit on the branch.  
⚙️ It provides methods for overwriting a new branch, ensuring a branch exists, checking if unstaged changes exist, committing changes, and getting the status of changes on the branch.  
📚 The class uses the `git` module to interact with the Git repository.  
📝 The `overwrite_new_branch` method creates a new branch, deletes an existing branch if it exists, and checks out the base branch.  
🔄 The `ensure_branch_exists` method checks if a branch exists, and if not, creates a new branch or checks out an existing remote branch.  
✅ The `unstaged_changes_exist` method checks if there are any unstaged changes on the branch.  
🔀 The `commit` method adds and commits changes, and can also push the branch to the remote repository.  


### [`diff_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/diff_service.py)

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


### [`platform_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/platform_service.py)

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


### [`publish_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/publish_service.py)

💡 This file contains the implementation of a service for publishing updates to a pull request description. It includes classes like `CodeBlock` and `UpdateSection` to represent different elements in the description. The main class is `PublishService`, which provides methods for updating and finalizing the pull request description. There are also subclasses `GitHubPublishService` and `DummyPublishService` for specific platforms.  


### [`trigger_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/trigger_service.py)

📚 This file contains a class called `TriggerService` which handles triggers for events.   
🔀 Triggers are objects that match specific events and execute workflows or actions in response.   
🔁 The `TriggerService` class has methods for handling triggers, executing workflows, and finalizing triggers.   
📣 Triggers and their associated contexts are gathered and processed to determine which workflows or actions to execute.   
🎬 The starting context for each trigger is logged and published.   
🏁 The final context after executing the workflow or action is also logged and published.   
🚀 The `trigger_event` method is the main entry point for triggering events and executing the associated workflows or actions.   
💡 The `finalize_trigger` method handles the finalization of triggers, including committing changes and merging PRs.   
📝 The file also includes helper methods for getting IDs and names for executables.  


### [`utils.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/utils.py)

💡 This file contains functions for formatting and truncating data for publishing.   
💡 The `truncate_strings` function truncates strings to a specified length and adds an ellipsis if necessary.   
💡 The `nested_to_dict` function converts nested objects (such as dictionaries and lists) to dictionaries.   
💡 The `format_for_publishing` function formats an object for publishing by converting it to a dictionary, truncating strings, and removing certain keys.   
💡 The file uses the `pydantic` library for working with data models.   
💡 The functions are designed to be used together to prepare data for display or publication.  


### [`workflow_service.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/services/workflow_service.py)

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
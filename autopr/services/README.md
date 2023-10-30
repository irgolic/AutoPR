

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains several Python files that provide various services for managing and running actions, caching data, working with commits and diffs in a Git repository, interacting with platforms like GitHub, publishing updates to pull requests, handling triggers, and executing workflows. These files define classes and methods that encapsulate the functionality related to each service, and they import other modules and dependencies as needed. The files are well-documented with comments explaining the purpose and functionality of each component.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/__init__.py)

This file is empty.  


### [`action_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/action_service.py)

📝 This file contains the implementation of the `ActionService` class, which is responsible for managing and running actions in the autopr system.  
🔧 It provides methods for finding, instantiating, and running actions.  
🔄 The `run_action` method runs a single action based on the provided action configuration.  
🔁 The `run_action_iteratively` method runs an action iteratively, either for a specified number of iterations or over a list in the context.  
📦 The class also includes helper methods for getting action inputs and extracting outputs.  
📚 The file imports various dependencies and other modules related to actions and services in the autopr system.  
💧 The file includes a class variable `ActionSubclass` and a commented-out inner class `Finished`.  
🔍 The file is well-documented with comments explaining the purpose and functionality of each method.  
❌ The file handles exceptions and logs errors when running actions, providing detailed error messages and traceback information.  


### [`cache_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/cache_service.py)

📝 The file defines a class called `CacheService` and a subclass called `ShelveCacheService`.  
📁 The `ShelveCacheService` class is a cache service that stores and retrieves data using the `shelve` module.  
💾 It has methods to store and retrieve data, with an optional namespace parameter.  
📂 The cache is stored in a directory specified by the `cache_dir` parameter.  
❗️ If the directory doesn't exist, it will be created.  
🔑 The default namespace is set to the `action_id` parameter provided during initialization.  
📝 The `_prepare_key` method converts the key to a string.  
📚 The `_load_shelf` method opens the shelve database file for the given namespace.  
✅ The `store` method stores the key-value pair in the shelve database.  
🔍 The `retrieve` method retrieves the value associated with the given key from the shelve database.  


### [`commit_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/commit_service.py)

📝 The file contains a class called `CommitService` that provides functionality for creating branches, committing changes, and pushing them to a Git repository.  
🔧 The class ensures that there is always a commit on the branch.  
📁 It imports necessary modules and defines a type alias `CHANGES_STATUS`.  
📜 The class has methods for overwriting a new branch, ensuring that a branch exists, making a commit, and getting the status of changes on the branch.  
🔄 The `overwrite_new_branch` method checks out and pulls the base branch, deletes an existing branch if it exists, creates a new branch, and makes an empty commit.  
🔄 The `ensure_branch_exists` method fetches from the remote repository, checks out and pulls the branch if it exists, or creates a local branch that tracks the remote branch if it doesn't exist.  
🔄 The `commit` method adds and commits changes, removes an empty commit if it exists, and pushes the branch to the remote repository.  
🔄 The `get_changes_status` method returns the status of changes on the branch, indicating if there are no changes, only cache changes, or modified changes.  
📜 The class uses a logger for logging debug and info messages.  


### [`diff_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/diff_service.py)

📝 This file contains the implementation of a DiffService class and its two subclasses: GitApplyService and PatchService.  
🔍 The purpose of this file is to provide functionality for getting and applying diffs in a git repository.  
🔧 The DiffService class has methods for getting and applying diffs, and it takes a git repository as a parameter.  
📁 The get_diff method retrieves the diff of the staged files in the repository, either for all files or specific file paths.  
✅ The apply_diff method applies the provided diff to the repository, either using the "git apply" command or the "patch" command.  
🌟 The GitApplyService subclass uses the "git apply" command to apply the diff.  
🌟 The PatchService subclass uses the "patch" command to apply the diff.  
📜 The diff is expected to be in the form of a string, represented by the DiffStr type alias.  
🔬 The apply_diff methods can also perform a dry run if the check parameter is set to True.  
📚 The file includes necessary imports and a logger for debugging purposes.  


### [`platform_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/platform_service.py)

📄 This file contains the implementation of two classes: `PlatformService` and `GitHubPlatformService`.   
🔧 The `PlatformService` class is a base class that defines the interface for making API calls to a platform, such as GitHub. It provides methods for interacting with issues, pull requests, comments, and more.  
🔒 The `GitHubPlatformService` class is a subclass of `PlatformService` that specifically interacts with the GitHub platform. It implements methods for creating and merging pull requests, updating pull request body and title, publishing comments, and more.  
🌟 The `GitHubPlatformService` class also includes additional functionality such as finding existing pull requests, closing pull requests and issues, and getting the URL of a file in the repository.  
📝 The file also includes a `DummyPlatformService` class, which is a placeholder implementation of `PlatformService` that does nothing. It can be used for testing or as a fallback when a platform-specific service is not available.  
❗️ Some methods in the classes are marked as `NotImplementedError`, indicating that they need to be implemented in subclasses.  
💡 The purpose of this file is to provide a standardized interface for making API calls to different platforms, with a specific implementation for GitHub. It allows for easy integration with different platforms and simplifies the process of interacting with issues, pull requests, and other platform-specific features.  


### [`publish_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/publish_service.py)

📄 This file contains the implementation of a service called `PublishService`.  
📝 The purpose of this service is to publish updates to the pull request description.  
🔄 It allows for controlling update sections and publishing updates and code blocks.  
📚 It includes classes for code blocks and update sections to organize the description.  
📝 The service can create child instances with their own sections and update hierarchy.  
🎯 The service can set the title and body of the pull request.  
📈 It can publish updates, code blocks, and start and end sections.  
✅ It can merge and close the pull request.  
🚀 The service supports publishing to GitHub and includes error reporting and progress tracking features.  


### [`trigger_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/trigger_service.py)

📜 This file contains the implementation of the `TriggerService` class.   
🔃 The class is responsible for handling triggers that are used to initiate workflows in a larger system.  
🔀 Triggers are defined as events that match certain conditions and are associated with executable actions or workflows.  
✨ The class provides methods for processing triggers, executing the associated actions/workflows, and handling the resulting context.  
📂 It also includes helper methods for retrieving information about the triggers and the associated executables.  
🔀 Triggers can be matched to events, and the corresponding actions/workflows can be executed asynchronously.  
📝 The class logs information about the loaded triggers and any errors that occur during execution.  
🔚 After executing the triggers, the class performs finalization steps based on the changes made and the automerge settings.  
📝 The class uses various services, such as `PublishService`, `WorkflowService`, and `CommitService`, to perform its tasks.  
🗂️ The file also includes imports for various modules and types used by the class.  


### [`utils.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/utils.py)

📝 This file contains functions for formatting Python objects for publishing.  
🔍 The `format_for_publishing` function takes an object and converts it into a formatted string in JSON format.  
✂️ The `truncate_strings` function is used to truncate long strings in the object to a specified length.  
🔍 The `nested_to_dict` function converts nested objects into dictionaries.  
🔍 The `format_for_publishing` function uses `nested_to_dict` to convert the input object to a dictionary and then applies string truncation and filtering of certain keys before converting it to JSON.  
📝 The purpose of this file is to provide utility functions for preparing data for publishing or display.  


### [`workflow_service.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/services/workflow_service.py)

📝 This file contains the implementation of a WorkflowService class, which is responsible for executing workflows and actions based on their IDs and inputs. It also provides methods for invoking workflows iteratively and validating inputs and outputs of workflows. The class uses other services such as ActionService and PublishService for running actions and publishing logs.  

<!-- Living README Summary -->
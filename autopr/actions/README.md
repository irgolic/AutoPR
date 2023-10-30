

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files that define various actions and utilities for an autonomous agent system. Each file represents a different action or utility, such as running a bash command, making API calls, publishing comments on GitHub issues, generating prompts using OpenAI's GPT-3 language model, and more. These files provide reusable functionality that can be used to perform specific tasks within the autonomous agent system.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/__init__.py)

📝 This file dynamically imports all modules in the same directory and subdirectories.  


### [`base.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/base.py)

📄 This file defines a base class and a metaclass for creating and registering actions in the autonomous agent system.   
🔒 The metaclass is responsible for registering actions in a global registry.  
🔑 The base class provides a structure for creating actions, with an ID, name, description, and a run method.  
📝 Actions are the basic unit of work in the system, performing a single task and returning a result.  
🔧 The base class also provides common attributes and services for actions to use.  
📚 The file also includes utility functions for getting the inputs and outputs types of actions, and retrieving the registered actions.  
📦 The file imports various modules and types used by the classes and functions defined in it.  


### [`bash.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/bash.py)

📝 This file contains a Python script that defines a class called "Bash" which is an action that can run a bash command and return its output.  
🔌 The "Bash" class inherits from a base class called "Action" and has two nested classes called "BashInputs" and "BashOutputs" which define the input and output models for the action.  
⚙️ The "run" method of the "Bash" class uses asyncio to run the bash command asynchronously and capture the standard output and standard error streams.  
💻 There is a main block that demonstrates how to manually run the "Bash" action using the provided utility function.  
📥 The input to the action is a bash command specified as a string.  
📤 The output of the action is the standard output and standard error of the bash command, both represented as strings.  
🔧 The purpose of this file is to provide a reusable action that can be used to run bash commands and capture their output in a Python program.  
🧪 The file includes a test utility for manually running the action and verifying its behavior.  
🏃‍♀️ To use this file, you can instantiate the "Bash" class and call its "run" method with the desired input command.  


### [`choice.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/choice.py)

📝 This file contains a Python script that defines a class called "Choice" which is used to generate a string prompt for making a choice from a list of options.   
🔢 It also defines two data models, "Inputs" and "Outputs", which represent the input and output structure for the "Choice" class.   
🔍 The script imports various modules and classes from external libraries such as openai, pydantic, and autopr.   
🔧 The "Choice" class has methods for building the prompt and instructions, invoking the choice, and running the action.   
🧪 The script includes a test case where the "Choice" class is manually run with predefined inputs.   
💾 The script also includes functionality for caching the results to improve performance.   
📚 The purpose of this file is to provide a reusable class for generating and making a choice from a list of options using the OpenAI API.   
📝 The file can be executed directly to run the test case.  


### [`comment.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/comment.py)

📄 This file contains a class called "Comment" which is an action to publish a comment on a GitHub issue.   
🔑 The class has an ID of "comment" and requires inputs such as a comment and an optional issue number.  
🚀 The "run" method in the class executes the action by publishing the comment using the provided inputs.  
💡 The class is a subclass of the "Action" class and uses the "publish_service" to publish the comment.  
📝 The class is defined using the Pydantic library for data validation.  
⚙️ The file imports necessary modules and types for the class and action to work.  


### [`commit_and_push.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/commit_and_push.py)

📄 This file defines a class called "CommitAndPush" that represents an action to commit and push changes to a remote repository.  
🔐 The class extends a base class called "Action" and is generic with inputs of type "Inputs" and no output.  
🔧 The "run" method within the class is async and takes an instance of "Inputs" as input.  
📝 The "commit_message" attribute of "Inputs" is set to "AutoPR commit" by default.  
📂 The "filepaths" attribute of "Inputs" is an optional list of strings.  
📥 The "run" method calls the "commit" method of a "commit_service" object with the commit message, filepaths, and push flag.  
📝 If the "filepaths" attribute is not provided, all changes are committed and pushed.  
📝 The "commit_and_push" identifier is used to distinguish this action from others.  
📄 The file uses the pydantic library for type validation and modeling of the "Inputs" class.  


### [`crawl_folder.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/crawl_folder.py)

📄 This file contains Python code for crawling a folder and listing its files and subfolders.   
🔎 The purpose of this code is to exclude certain files and directories from the crawl.  
⚙️ It uses regular expressions to define patterns for files and directories to ignore.  
📥 The code takes inputs such as the folder path, files and subfolders to ignore, and whether to ignore binary files.  
📤 It returns the contents of the crawled folder and the URL of the folder to crawl.  
🔒 The code also checks if a file is binary or not before including it in the results.  
📂 The main function runs the action manually, passing the necessary inputs.  
🚀 The file can be executed as a standalone script or imported as a module.  
💡 The purpose of the action is to provide a convenient way to crawl folders and retrieve their contents while excluding certain files and directories.  


### [`find_todos.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/find_todos.py)

📝 The purpose of this file is to scan through all files in a directory and its subdirectories, find comments with "#TODO" or "#FIXME" in them, and print them out in a list with the task, filepath, and line number.  


### [`insert_content_into_text.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/insert_content_into_text.py)

📝 This file contains a Python class called "InsertContentIntoText" that represents an action.      
🔍 The purpose of this action is to insert content into a string at a specified delimiter.       
📋 The action takes inputs such as the existing content, delimiter, and content to add.       
✨ If the delimiter occurs only once in the string, the content is appended to the end of the string with delimiters.       
✨ If the delimiter occurs two or more times, the content is inserted between the last two delimiters.       
🔧 The action provides a method called "insert_tag_content_into_string" to perform the insertion.       
🔄 The method counts the occurrences of the delimiter in the file content and determines the appropriate insertion strategy.       
💾 The action is implemented as an asynchronous function called "run" that takes the inputs and returns the outputs.       
🔬 The file also includes two examples demonstrating how to use the action.       
🧪 The examples test different scenarios, including no delimiters and two delimiters.  


### [`make_api_call.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/make_api_call.py)

📝 This file contains a Python script for making an API call and returning the response.   
📝 The script defines two classes: `Inputs` and `Outputs`, which represent the input and output data for the action.   
📝 The main class `GetApiCallActions` is responsible for making the API call and handling the response.   
📝 The `run` method of `GetApiCallActions` sends an HTTP GET request to the specified `endpoint_url` with optional headers.   
📝 If the API call is successful (status code 200), the response content is returned as a string.   
📝 If the API call fails, an exception is raised with the corresponding status code.   
📝 The script also includes a condition to run the action manually when the file is executed directly.   
📝 The action is manually executed with predefined inputs, including the `endpoint_url` and `headers`.   
📝 The script imports necessary modules and defines the required dependencies.   
📝 The purpose of this file is to provide a reusable action that can be used to make API calls and retrieve the response.  


### [`prompt.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/prompt.py)

📝 This file contains code for generating a string using OpenAI's GPT-3 language model.  
🤖 The purpose of the file is to provide a prompt-based interface to generate text responses.  
📥 It imports various libraries and modules required for the functionality.  
🧩 The code defines a `PromptString` class that extends a base `Action` class.  
🔧 The class has methods for building the prompt and instructions, and for running the prompt generation.  
📝 It uses a cache to store and retrieve previously generated results.  
🔀 The code includes a conditional block for manual execution when the file is run directly.  
🍎 The example at the end demonstrates how to use the `PromptString` class to generate a fruit salad prompt.  
🔍 The generated prompt and instructions are displayed, and the result is returned as an output.  


### [`publish_issue.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/publish_issue.py)

📝 This file contains a Python script for publishing or updating an issue on a platform.  
📌 It defines the `Inputs` and `Outputs` models for the action.  
🔍 The `PublishIssue` class is the main action that handles the publishing or updating of the issue.  
🔧 It uses the `platform_service` to interact with the platform's API.  
📄 The `run` method checks if the issue exists and either creates or updates it based on the inputs.  
🔀 The script can be run directly to manually test the action.  
⚠️ The `PlatformService.publish_issue` method is mocked for testing purposes.  
🔧 The action is triggered with sample inputs provided in the `__main__` block.  
📦 The script imports various modules and classes required for its functionality.  
📄 The file is organized with appropriate imports, class definitions, and a conditional execution block.  


### [`read_file.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/read_file.py)

📝 This file contains a class called `ReadFile` that represents an action to read the contents of a file.  
📂 The class has methods to load the contents of a Jupyter notebook file and to ensure that a file exists at a given file path.  
📄 The `run` method of the class reads the contents of a file and returns them along with the success status and the URL of the file in the repository.  
🔒 The class is defined as a subclass of the `Action` class from a module called `autopr.actions.base`.  
⚙️ The `Inputs` and `Outputs` classes define the input and output data models for the `ReadFile` action.  
🔍 The `ensure_file_exists` method creates an empty file at a given file path if it doesn't already exist.  
📚 The `load_jupyter_notebook` method extracts the content from a Jupyter notebook file, including markdown cells and code cells with their outputs.  
⚠️ If an error occurs while reading the file, an error message is logged and the error is raised.  
🔧 The file also includes a test case that manually runs the `ReadFile` action and removes the test file afterwards.  


### [`search.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/search.py)

📝 This file contains a Python script for searching files in a directory and its subdirectories for a given query.  
🔍 It uses the `Search` class, which extends a base `Action` class and has a `run` method for executing the search.  
📂 The search can be performed in a specific directory or the current working directory if no directory path is provided.  
🔑 The query to search for is specified in the `Inputs` class, along with an optional directory path and entries to ignore.  
📥 The search results are returned as a list of `SearchHit` objects in the `Outputs` class.  
🔧 The search is performed by iterating over all files in the directory and its subdirectories using the `os.walk` function.  
🚫 Certain files and directories can be ignored during the search by specifying them in the `entries_to_ignore` field.  
📄 Each file is opened and searched line by line, and any matches are stored as `SearchHit` objects with the file path, line number, and character number.  
🔄 The search results are sorted by file path, line number, and character number before being returned.  
🏃‍♂️ The script can be run directly, executing the search with predefined inputs by using the `run_action_manually` function.  


### [`set_issue_title.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/set_issue_title.py)

📝 This file defines a class called "SetIssueTitle" that represents an action to set the title of an issue.   
📦 It uses the pydantic library for input validation.   
🔑 The action has an "id" attribute set to "set_issue_title".   
⚡️ The action's "run" method takes an "Inputs" object as input and sets the title of an issue using the "publish_service" attribute.   
🎯 The purpose of this file is to provide a reusable action for setting the title of an issue.  


### [`utils/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/utils)

This folder contains two files: "__init__.py" and "prompt_context.py". The "__init__.py" file is empty. The "prompt_context.py" file is used for managing and transforming prompt context in a natural language processing application. It includes classes and functions for working with prompt context entries and configurations, as well as functions for trimming the context and invoking OpenAI's Chat Completion API.  


### [`write_into_file.py`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr/actions/write_into_file.py)

📝 This file contains a Python script that defines a class called `WriteIntoFile`.  
🖊️ The purpose of this class is to write content into a file.  
🔑 The class has an `id` attribute set to "write_into_file".  
📥 It has an `async` method called `run` that takes an `Inputs` object as input and returns an `Outputs` object.  
📄 The `Inputs` class defines the required input parameters for the `run` method, such as the filepath, content, and whether to append or replace the file content.  
✍️ The `Outputs` class defines the output parameter, which is a boolean indicating whether the file was written to successfully.  
🔧 The `run` method checks if the filepath is relative to the repository root and creates the necessary directories if they don't exist.  
📝 It then opens the file and writes the content based on the append or replace option.  
✅ Finally, it returns an `Outputs` object with a success flag indicating the success of the write operation.  
🔬 The script also includes a test case that demonstrates the usage of the `WriteIntoFile` class.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files and a subfolder. The files define various actions and utilities for performing tasks in an autonomous agent system. These actions include tasks such as running Bash commands, generating choices based on user prompts, publishing comments on GitHub issues, committing and pushing changes to a remote repository, searching for specific keywords in files, and more. The subfolder contains a file that provides functionality for managing prompt context in a conversational AI system. Overall, the files in this folder provide a set of reusable actions and utilities for automating tasks in different contexts.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/__init__.py)

📁 This file is used to automatically import all modules within the same directory.    
🔍 It identifies all Python files and directories within the current directory.    
🔌 It imports all the Python files as modules.    
📂 It imports all the directories as modules.    
📚 The purpose is to make it easier to import and use the contents of this directory.  


### [`base.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/base.py)

📋 This file defines a base class and metaclass for actions in an autonomous agent system.  
🔍 The purpose of the file is to provide a framework for creating and registering actions.  
🔧 Actions are responsible for performing tasks, affecting the environment, and returning results.  
🔒 The metaclass registers actions in a global registry based on their ID.  
✨ The base class provides a run method for executing the action and an init method for initializing dependencies.  
🌟 The file also includes a function for retrieving a dictionary of registered actions.  


### [`bash.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/bash.py)

📝 This file defines a Bash action class that runs a bash command and returns its output.  


### [`choice.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/choice.py)

📄 This file contains the implementation of a Python class called "Choice".    
🔀 The "Choice" class is an action that prompts the user to make a choice from a given list.    
📝 It takes various inputs such as the list of choices, whether multiple choices are allowed, the model to use for generating the prompt, and more.    
📜 The class has methods for building the prompt and instructions, invoking the choice generation using OpenAI, and caching the results.    
🔄 It uses other modules and classes from the project, such as "Action", "PromptContext", and "trim_context".    
🔧 The main function at the end of the file demonstrates how to manually run the "Choice" action with sample inputs.    
✨ The purpose of this file is to provide a reusable and configurable action for generating choices based on user prompts.    
🌟 It leverages OpenAI's language model to generate the choices and provides flexibility in terms of the choice options and input parameters.    
📚 The file also includes type annotations and Pydantic models for input and output data.  


### [`comment.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/comment.py)

📄 This file defines a class called "Comment" that represents an action to publish a comment on a GitHub issue.  
🔑 The class has an "id" attribute set to "comment".  
🔗 The class inherits from a generic "Action" class and specifies the input and output types for the action.  
📝 The input type is defined as a Pydantic model called "Inputs" with a required "comment" field and an optional "issue_number" field.  
🔀 The "run" method of the "Comment" class executes the action by publishing a comment using a publish service.  
👥 The "run" method takes an instance of the "Inputs" model as its input.  
🌐 The "publish_service" used to publish the comment is not defined in this file and is likely imported from elsewhere.  
💡 The file is part of a larger codebase that implements a system for automating actions on GitHub issues.  
📖 The purpose of this file is to define the "Comment" action and its associated input model.  


### [`commit_and_push.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/commit_and_push.py)

📝 This file defines a class called "CommitAndPush" that represents an action to commit and push changes to a remote repository.  
📝 The class has an "id" attribute set to "commit_and_push".  
📝 The class has a "run" method that takes an instance of "Inputs" as input and returns None.  
📝 The "run" method calls the "commit" method of the "commit_service" attribute with the commit message, file paths, and push flag from the input.  
📝 The "commit_service" attribute is not defined in this file.  
📝 The "Inputs" class is defined as a pydantic model with two attributes: "commit_message" and "filepaths".  
📝 The "commit_message" attribute has a default value of "AutoPR commit".  
📝 The "filepaths" attribute is an optional list of strings and has a default value of None.  
📝 The file has some import statements, including one for the "Action" class from "autopr.actions.base" module.  
📝 The file has a docstring that provides a brief description of the "CommitAndPush" class.  


### [`find_todos.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/find_todos.py)

📝 This file is a Python script that scans through files in a directory and its subdirectories to find comments containing specific keywords like "TODO" or "FIXME".   
🔍 It uses Tree-sitter to parse the files and extract the comments.   
📄 The script then prints out a list of the comments along with their tasks, file paths, and line numbers.   
🔗 It also provides URLs to the specific locations in the files where the comments are found.   
📋 The script can be run standalone, and it includes a main function that demonstrates how to run it manually.  


### [`insert_content_into_text.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/insert_content_into_text.py)

📝 This file contains a Python class called "InsertContentIntoText" that implements an action for inserting content into a string at a specified delimiter.  
🖊️ The class takes inputs such as the existing content, delimiter, and content to add.  
🔍 It counts the occurrences of the delimiter in the existing content and determines the appropriate insertion behavior.  
✅ If there are no delimiters or only one delimiter, the content is appended at the end with delimiters.  
✅ If there are two or more delimiters, the content is inserted between the last two delimiters.  
🔀 The class has a "run" method that executes the insertion logic and returns the updated content.  
🚀 The file also includes example usage of the class, demonstrating how to run the action manually with different inputs.  
🧪 The examples cover scenarios with no delimiters and two delimiters.  
📚 The file imports necessary modules and defines data models for inputs and outputs.  
💡 The purpose of this file is to provide a reusable action for inserting content into a string at a specified delimiter.  


### [`list_folder.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/list_folder.py)

📄 This file contains the implementation of a Python class called "ListFolder".  
📂 The purpose of this class is to list all the files and subfolders in a given folder, excluding certain files and directories.  
🔍 It provides functionality to ignore specific files and subfolders during the crawl.  
🔗 The class also returns the URL of the crawled folder.  
📦 It uses external libraries such as asyncio, re, and pydantic.  
🗂️ The class defines a data model for the inputs and outputs using the BaseModel class from pydantic.  
🔧 The class has a static method to check if a file is binary.  
🔄 The main function of the file runs the ListFolder action manually with the provided inputs.  
🔗 The ListFolder class is part of a larger codebase, as indicated by the import statements and the conditional execution check at the end of the file.  


### [`make_api_call.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/make_api_call.py)

📝 This file contains a Python script that makes an API call to a specified endpoint URL.  
📦 It defines two classes, `Inputs` and `Outputs`, which represent the input and output data for the API call action.  
🔌 The `GetApiCallActions` class is a subclass of the `Action` class, and it implements the logic for making the API call.  
🔧 The `run` method of the `GetApiCallActions` class sends an HTTP GET request to the specified endpoint URL with the provided headers.  
✅ If the API call is successful (status code 200), it returns the contents of the response as a string.  
❌ Otherwise, it raises an exception with the corresponding status code.  
⚙️ The file also includes a `main` block that demonstrates how to manually run the action with some sample inputs.  
🧪 It imports the necessary utilities from the `autopr.tests.utils` module.  
🔽 The API endpoint URL and headers are provided as inputs to the `run_action_manually` function, which executes the action using asyncio.  


### [`prompt.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/prompt.py)

📝 This file contains a Python script that defines a class called "PromptString".  
🔍 The purpose of the file is to generate a string prompt using OpenAI's GPT-3.5 Turbo model.  
🔧 The script takes various inputs, such as the model to use, the prompt context, instructions, and more.  
📥 It uses these inputs to build a prompt and instructions for the model.  
🚀 The script then runs the model with the prompt and instructions to generate a response.  
💾 The generated response is cached to avoid unnecessary API calls.  
📤 The response is returned as the output of the script.  
📚 The script also includes a main block for testing the "PromptString" class.  
🔧 The main block creates an instance of the class and runs it with sample inputs.  
👀 The output of the script is printed to the console.  


### [`publish_issue.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/publish_issue.py)

📝 This file contains Python code for publishing or updating an issue on a platform.  
🔍 It defines a class called `PublishIssue` which is responsible for creating or updating issues.  
✨ The class is a subclass of `Action` and uses `BaseModel` from `pydantic` for input and output validation.  
🔧 The `run` method of `PublishIssue` is responsible for executing the logic based on the input parameters.  
👥 The class has two nested classes, `Inputs` and `Outputs`, which define the structure of input and output data.  
📦 It imports various modules and classes from external libraries.  
🎯 The main block of the file demonstrates how to manually run the `PublishIssue` action with test inputs.  
🛠️ The `PlatformService` class is used for interacting with the platform to create or update issues.  
🧪 The file also includes a mock for the `publish_issue` method of `PlatformService` for testing purposes.  
💡 The purpose of this file is to provide a reusable action for publishing or updating issues on a platform.  


### [`read_file.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/read_file.py)

📝 This file contains a class called "ReadFile" which represents an action to read the contents of a file.   
🔍 It has a static method to load the contents of a Jupyter notebook file and another static method to ensure a file exists at a given file path.   
📂 The class has an async method "run" that reads the contents of a file and returns the contents, success status, and URL of the file.   
📚 The file also includes a BaseModel for inputs and outputs, as well as some utility functions.   
💡 It can be run directly to test the "ReadFile" action.  


### [`search.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/search.py)

📝 This file defines a class called "Search" that performs a search for a given query in all files within a specified directory and its subdirectories.   
📂 The search is performed by iterating through each file, reading its contents, and checking if the query is present in any line.   
💼 The search results are stored in a list of SearchHit objects, which contain information about the file path, line number, and character number where the query was found.   
🔍 The search can be customized by specifying a directory path to search in and a list of entries to ignore (both files and directories).   
🔧 The search functionality is encapsulated within the Search class, which inherits from a base Action class.   
📥 The inputs to the Search action include the query, directory path, and entries to ignore.   
📤 The outputs of the Search action include the list of search hits.   
📚 The Search class also includes a helper method for searching a single file.   
🧹 The search results are sorted based on the file path, line number, and character number.   
🏃‍♀️ The file can be run as a standalone script to execute the search action manually.  


### [`set_issue_title.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/set_issue_title.py)

📄 This file defines a class called `SetIssueTitle` which is an action to set the title of an issue.  
🔑 The class has an `id` attribute with the value "set_issue_title".  
🔧 The class has an async method called `run` which takes an instance of `Inputs` as input and doesn't return anything.  
📦 The `Inputs` class is defined in this file and has a single attribute called `title` of type `str`.  
🧪 The `run` method calls a method called `set_title` on a `publish_service` object, passing in the `title` from the `Inputs` object.  
📝 The `SetIssueTitle` class is a subclass of a generic `Action` class.  
🔗 The `Action` class is imported from a module called `base` in a package called `autopr.actions`.  
💡 The purpose of this file is to define the logic for setting the title of an issue using the `publish_service`.  
📚 This file uses the `pydantic` library to define the data model for the `Inputs` class.  


### [`utils/`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/utils)

This folder contains two files. The `__init__.py` file is empty. The `prompt_context.py` file provides functionality for managing and manipulating prompt context in a conversational AI system. It defines classes and functions for representing and manipulating prompt context, trimming the context if it exceeds a specified token length, calculating the token length of a string for a given model, and invoking the OpenAI Chat Completion API. The file also includes import statements and uses external libraries such as `pydantic`, `tenacity`, and `tiktoken`.  


### [`walk_files.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/walk_files.py)

📂 This file contains code for listing files and subfolders in a given folder.  
🔍 It excludes certain files and directories based on predefined patterns.  
🗂️ The code uses regular expressions to match and ignore specific file patterns.  
📝 The code defines two Pydantic models: Inputs and Outputs, to specify the input and output data structures.  
⚡️ The main action defined in the code is "WalkFiles", which performs the file crawling and filtering.  
🔒 It has an optional flag to ignore binary files during the crawl.  
📥 The Inputs model specifies the folder path, files to ignore, and the binary files flag.  
📤 The Outputs model returns the list of files and subfolders found in the specified folder.  
🚀 The code includes a sample usage of the WalkFiles action using asyncio.  
📚 The code also includes import statements and a main block for manual execution/testing.  


### [`write_into_file.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/actions/write_into_file.py)

📝 This file defines a class called "WriteIntoFile" that is responsible for writing content into a file.   
🔒 It imports necessary modules and defines input and output models using Pydantic.  
⚙️ The class has an async "run" method that performs the actual writing operation.  
📝 The purpose of this file is to provide a reusable action for writing content into a file.  
🗂️ It handles both appending content to the end of the file and replacing the entire file content.  
🔒 It checks if the given file path is relative to the repository root and raises an error if it is not.  
🗂️ It creates the necessary directories if they don't exist.  
⌨️ It uses the "open" function to open the file and writes the content into it.  
🔀 The "run" method returns an output model indicating whether the file was written to successfully.  
🔀 The file includes a test case that demonstrates how to use the "WriteIntoFile" action.  

<!-- Living README Summary -->
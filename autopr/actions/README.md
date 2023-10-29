

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python files that serve different purposes. The files include modules for importing and organizing other Python files, base classes for defining actions in an autonomous agent system, scripts for running bash commands and making API calls, classes for generating prompts and searching for specific content, and utilities for managing prompt context in a chatbot application. There are also files for reading and writing file contents, publishing comments and issues on platforms, and finding and managing TODO tasks in code. Overall, this folder provides a variety of reusable components for building automation and AI-related tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/__init__.py)

📂 The file imports modules from the current directory.  
🧩 It gathers all Python files in the directory and imports them.  
📚 It also imports all modules from subdirectories.  
📄 The imported modules are stored in the "__all__" variable.  
🔍 The purpose of the file is to make all modules easily accessible.  


### [`base.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/base.py)

📄 This file defines a base class for actions in an autonomous agent system. Actions are responsible for performing tasks, affecting the environment, and returning results.  
🔍 The file also contains a metaclass for registering actions in a global registry.  
📝 The base class has attributes for the ID, name, and description of an action.  
🔀 The base class is generic and can take input and output types.  
🏭 The base class has a run method that needs to be implemented by subclasses.  
🔧 The base class has an initializer that takes various services and a logger.  
🔢 The base class has methods for getting the input and output types.  
🔍 The file includes a function that returns a dictionary of all registered actions.  
🔀 The file imports various modules and types that are used throughout the code.  


### [`bash.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/bash.py)

📝 This file contains a Python script for running a bash command and returning its output.   
🔧 It defines a class called "Bash" that extends a base class called "Action".  
📥 The "Bash" class has a method called "run" which takes a command as input and executes it using asyncio.  
📤 The output of the command is captured and returned as a string.  
💡 The purpose of this file is to provide a reusable component for running bash commands in Python scripts.  
🚀 The script can be run independently to manually test the "Bash" action with a predefined command.  
🔧 The file imports necessary modules and defines input and output models for the "Bash" action.  
🔬 The file also includes a conditional block that runs the "Bash" action with a sample command when the file is executed directly.  
🧪 The file can be used as a starting point for building more complex automation tasks involving bash commands.  


### [`choice.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/choice.py)

📝 This file contains a Python script for generating a choice prompt using OpenAI's GPT-3.5 model.  
🤖 The purpose of the script is to create a helpful assistant that can make a choice from a given list of options.  
🔢 It takes input parameters such as the list of choices, model to use, prompt context, instructions, and temperature.  
🔀 The script builds a prompt and instructions based on the input parameters and invokes the OpenAI model to generate a choice.  
🗒️ The generated choice is then validated against the input choices and returned as the output.  
📚 It also includes functions for caching and publishing the generated output and code blocks.  
📝 The script provides a main function for manually running the choice action with predefined inputs.  
🍎 The example at the end demonstrates how to use the script to generate a choice prompt for making a fruit salad.  
🔒 The script uses asyncio for asynchronous execution and pydantic for data validation.  
📄 The script imports necessary modules and defines the required data models and classes.  


### [`comment.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/comment.py)

📄 This file defines a class called "Comment" which represents an action to publish a comment on a GitHub issue.  
🔑 The class has an ID of "comment" and inherits from the "Action" class.  
🔍 The class has an asynchronous method called "run" which takes an instance of "Inputs" as input and returns None.  
📝 The "Inputs" class is a Pydantic BaseModel that defines the input parameters for the "Comment" action.  
🗒️ The input parameters include a "comment" (str) and an optional "issue_number" (int).  
⚙️ The "run" method calls the "publish_comment" method of the "publish_service" to publish the comment on the specified issue.  
📚 The file imports necessary modules and packages like "typing" and "pydantic".  
✅ The file is part of a larger codebase and serves the purpose of implementing a specific action in an automated process.  


### [`commit_and_push.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/commit_and_push.py)

📄 This file defines a class called "CommitAndPush" that represents an action to commit and push changes to a remote repository.  
🔐 The class extends a base class called "Action" and is generic with inputs of type "Inputs" and no output.  
🔧 The "run" method within the class is async and takes an instance of "Inputs" as input.  
📝 The "commit_message" attribute of "Inputs" is set to "AutoPR commit" by default.  
📂 The "filepaths" attribute of "Inputs" is an optional list of strings.  
📥 The "run" method calls the "commit" method of a "commit_service" object with the commit message, filepaths, and push flag.  
📝 If the "filepaths" attribute is not provided, all changes are committed and pushed.  
📝 The "commit_and_push" identifier is used to distinguish this action from others.  
📄 The file uses the pydantic library for type validation and modeling of the "Inputs" class.  


### [`crawl_folder.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/crawl_folder.py)

📄 This file defines a class called "CrawlFolder" that lists the files and subfolders in a given folder while excluding certain files and directories.  
📂 The class takes inputs such as the folder path, a list of entries to ignore, and whether to ignore binary files.  
🔍 It uses regular expressions to filter out non-informative files and directories.  
💻 The class has a method to check if a file is binary.  
🔗 It returns the list of file entries and the URL of the folder being crawled.  
🚀 The file also contains a main function that manually runs the "CrawlFolder" action using the provided inputs.  
💡 The purpose of the file is to provide a way to crawl and filter the contents of a folder.  
📚 The file imports various modules and defines a couple of data models.  
🔧 It utilizes the "autopr" and "pydantic" libraries for its functionality.  
🔒 The file does not have any test cases included.  


### [`find_todos.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/find_todos.py)

📝 This file contains the implementation of a class called "FindTodos".  
🔍 The purpose of this class is to scan through all files in a directory and its subdirectories, find comments with "#TODO" or "#FIXME" in them, and return a list of tasks along with their file paths and line numbers.  
✅ It also provides methods for filtering out closed issues and closing unused issues related to the found todos.  
🔧 The class uses the Tree-sitter library for parsing files and supports multiple programming languages.  
📦 It imports various modules and classes from external libraries.  
🔑 The main entry point of the file is the `run` method, which executes the scanning process and returns the list of todos.  
⚙️ The file also includes some utility models and functions used by the main class.  
🚧 The file includes a test case that demonstrates how to run the `FindTodos` action manually.  
📚 The file is well-documented with docstrings and comments to explain the functionality of each component.  
🛠️ The file can be used as a standalone script or as part of a larger codebase for automated code review or task management purposes.  


### [`insert_content_into_text.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/insert_content_into_text.py)

📄 This file contains a Python script for inserting content into a string at a specified delimiter.  
🔍 The purpose of the script is to insert content into a string based on the occurrence of a delimiter.  
🔧 It provides a class called "InsertContentIntoText" which has a method for inserting the content.  
⚙️ The method checks the number of occurrences of the delimiter in the string.  
✏️ If there are no or only one occurrence, the content is appended to the end with delimiters.  
✏️ If there are two or more occurrences, the content is inserted between the last two delimiters.  
📥 The script also defines input and output models for the action.  
🔬 There are two examples provided to demonstrate the functionality of the script.  
🧪 The script can be manually tested using the "run_action_manually" function from the test utils module.  
📖 Overall, this script provides a convenient way to insert content into a string at a specific delimiter.  


### [`make_api_call.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/make_api_call.py)

📝 This file defines an action class called "GetApiCallActions" that makes an API call to a specified endpoint URL and returns the response.  
🔌 The action takes inputs such as the endpoint URL and optional headers.  
💼 It uses the "requests" library to make the API call.  
📥 If the API call is successful (status code 200), it returns the contents of the response.  
❌ Otherwise, it raises an exception with the corresponding status code.  
🔧 The action class is generic and extends a base class called "Action" from the "autopr.actions.base" module.  
🔄 The action can be manually run by executing the file.  
🔍 It includes a test utility function called "run_action_manually" from "autopr.tests.utils" to facilitate manual testing.  
🌐 The example endpoint URL used in the code is "https://jsonplaceholder.typicode.com/todos".  
🔑 The headers can be customized to include additional information in the API request.  


### [`prompt.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/prompt.py)

📝 This file contains code for generating a string using the OpenAI GPT-3 model.  
🔤 It defines the `Inputs` and `Outputs` models for the prompt generation.  
🖋️ The `PromptString` class is responsible for building the prompt and instructions, and running the prompt generation.  
🔍 It checks the cache for previously generated prompts before generating a new one.  
💾 The generated prompts are stored in the cache for future use.  
🍎 The example at the bottom demonstrates how to use the `PromptString` class to generate a prompt for making a fruit salad.  
🔑 The `PromptString` class is identified by the ID "prompt".  
🔧 It depends on various imports and helper functions.  
📚 The purpose of this file is to provide a reusable component for generating prompts using the GPT-3 model.  


### [`publish_issue.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/publish_issue.py)

📄 This file contains code for publishing or updating an issue on a platform.   
🔍 It checks if the issue with the specified title already exists.   
✏️ If the issue doesn't exist, it creates a new issue with the specified title, body, and labels.   
✏️ If the issue exists and the 'update_if_exists' flag is set to True, it updates the issue with the specified body and labels.   
📥 The inputs for this action include the issue title, body, labels, and the 'update_if_exists' flag.   
📤 The output of this action is the issue number of the published/updated issue.   
🧪 The code also includes a test case where the 'publish_issue' method is mocked for testing purposes.  


### [`read_file.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/read_file.py)

📝 The file contains a Python class called "ReadFile" that represents an action to read the contents of a file.  
📄 It imports necessary modules and defines two Pydantic models for input and output data.  
🔍 The "load_jupyter_notebook" method is used to read the contents of a Jupyter notebook file.  
✅ The "ensure_file_exists" method ensures that a file exists at the given file path.  
🔧 The "run" method is the main function that reads the contents of a file based on the input parameters.  
🚀 It can handle both regular text files and Jupyter notebook files.  
📑 The "contents" of the file, the "success" status, and the "url" of the file in the repository are returned as outputs.  
❗️ If any unexpected error occurs during file reading, it will be logged and raised.  
🔬 There is a test section at the end that demonstrates how to manually run the "ReadFile" action.  


### [`search.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/search.py)

📄 This file contains a Python script for searching for a given query across all files in a directory and its subdirectories.  
🔍 The script defines a class called "Search" that inherits from a base class called "Action".  
🔑 The "Search" class has an async method called "run" which performs the search operation.  
📥 The search inputs include the query string, directory path, and a list of entries to ignore.  
📤 The search outputs include a list of "SearchHit" objects containing the file path, line number, and character number of each hit.  
📂 The search is performed by recursively walking through the directory and its subdirectories, excluding the specified entries to ignore.  
🔍 Each file is opened and searched line by line to find matches with the query.  
📃 The hits are sorted based on the file path, line number, and character number.  
🚀 The script can be run independently by executing the main block at the end of the file.  


### [`set_issue_title.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/set_issue_title.py)

📝 This file defines a class named `SetIssueTitle` which represents an action to set the title of an issue.   
📋 The class is a subclass of `Action` and takes an input of type `Inputs` which has a single field `title` of type `str`.   
💻 The `run` method of the class is an asynchronous function that sets the title of an issue using the `publish_service` object.   
🔑 The class has a unique identifier `id` which is set to "set_issue_title".  


### [`utils/`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/utils)

This folder contains Python code for managing prompt context in a chatbot application. The `prompt_context.py` file defines a `PromptContext` class that represents a dictionary mapping headings to context variable values. It provides methods for formatting the context as a string and calculating the token length. The file also includes declarations for prompt context in a config file and functions for trimming the context and invoking the OpenAI Chat Completion API.  


### [`write_into_file.py`](https://github.com/raphael-francis/AutoPR-internal/blob/abf8a94706cbed9949282f3ad09945acb09227e5/./autopr/actions/write_into_file.py)

📝 The purpose of this file is to define an action called "WriteIntoFile" that writes content into a file.  
🔒 The action requires the filepath, content, and append_at_the_end parameters.  
⚙️ The action checks if the filepath is relative to the repository root and creates the necessary directories if they don't exist.  
📝 The action then opens the file and writes the content either at the end or replaces the entire file content.  
✅ The action returns a success flag indicating whether the file was written to successfully.  
🔧 The file also includes a test case to manually run the action.  

<!-- Living README Summary -->
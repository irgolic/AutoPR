

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various files and modules that define actions and utilities for different tasks. These actions include dynamically importing modules, performing actions in an autonomous agent system, running bash commands, publishing comments on GitHub issues, committing and pushing changes to a remote repository, crawling folders and filtering files, inserting content into a text string, generating prompts using OpenAI's GPT-3 language model, reading file contents, setting the title of an issue, and writing content into a file. The files provide reusable code for automating these tasks and can be used in larger projects or workflows.


### `__init__.py`

📂 This file is used to dynamically import all modules in its directory.  
📝 It retrieves the file and directory names using the `glob` module.  
🔍 It filters out the files and directories that are not Python modules.  
📚 It creates a list of module names by removing the file extensions.  
📁 It also includes the names of directories with an `__init__.py` file.  
🔀 The `__all__` variable is set to include all the module and directory names.  
🔗 The `from . import *` statement imports all the modules in this file's directory.  
🙅‍♀️ The `pyright: ignore[reportUnsupportedDunderAll]` comment suppresses an error message.  
📑 The purpose of this file is to provide a convenient way to import all modules in its directory.  
📌 It allows for easy organization and modularization of code.


### `base.py`

📄 This file defines a base class for actions in an autonomous agent system.
🧩 Actions are responsible for performing a single task and returning a result.
🔑 The file also includes a metaclass for registering actions in a global registry.
🔧 The base action class provides a run method and initializes various services.
📝 The file includes methods for getting the input and output types of an action.
📚 There is a function that returns a dictionary of registered actions.



### `bash.py`

📝 This file is a Python script that defines a class called `Bash` which is an implementation of an action. 
🔧 The purpose of the `Bash` action is to run a bash command and return its output. 
🔌 The action takes a command as an input and returns the standard output and standard error as outputs. 
🔍 The file also defines input and output models for the `Bash` action. 
🔬 The `Bash` action is executed when the file is run as a standalone script. 
🚀 The script uses the `asyncio` library to run the action asynchronously. 
⚙️ The `run` method of the `Bash` class uses the `asyncio.create_subprocess_shell` function to run the bash command. 
📥 The standard output and standard error streams are captured using the `communicate` method of the subprocess object. 
📤 The output values are then returned as an instance of the `BashOutputs` class. 
📌 The file also includes a test that manually runs the `Bash` action with a sample command.


### `comment.py`

📄 This file contains a class called `Comment` that represents an action to publish a comment on a GitHub issue.
🔑 The class has an `id` attribute set to "comment".
📝 The class has a `run` method that takes inputs of type `Inputs` and returns `None`.
📥 The `Inputs` class is a Pydantic model that defines the expected inputs for the `Comment` action.
🗒️ The `Inputs` class has two attributes: `comment` (a required string) and `issue_number` (an optional integer).
🔀 The `issue_number` attribute has a default value of `None`.
💻 The `run` method calls a `publish_comment` method from a `publish_service` to publish the comment on the GitHub issue.
📥 The `publish_comment` method takes the comment and issue number as inputs.
📚 The file imports necessary modules and inherits from a base `Action` class.
🌟 The file is part of a larger codebase for automating actions on GitHub issues.


### `commit_and_push.py`

📄 The file contains a class named "CommitAndPush" which represents an action to commit and push changes to a remote repository.
🔑 The class has an ID attribute assigned as "commit_and_push".
🔀 The class inherits from a base class named "Action" and specifies the generic type "Inputs" for input parameters and "None" for output.
🔧 The class has an async method named "run" which takes an instance of "Inputs" as input and returns None.
📌 The "run" method calls the "commit" method of a "commit_service" object, passing the commit message, filepaths, and a push flag.
📝 The default commit message is set to "AutoPR commit".
📂 The "filepaths" attribute of "Inputs" is an optional list of strings.
⚙️ The file uses the "pydantic" library for input validation.
🔍 The file imports necessary modules and packages.
💡 The purpose of the file is to define and implement the logic for committing and pushing changes to a remote repository.


### `crawl_folder.py`

📄 This file contains code for crawling a folder and listing its files and subfolders. 
🔍 It excludes certain files and directories based on predefined patterns.
🧪 The code includes a class `CrawlFolder` which is an action that can be run manually.
📥 The action takes inputs such as the folder path, files and subfolders to ignore, and whether to ignore binary files.
✅ It returns the list of file entries in the specified folder after applying the exclusion criteria.
⚠️ The exclusion criteria include patterns for files and directories that are considered non-informative.
🔧 The code also includes a utility function `is_binary` to check if a file is binary.
🔌 The code has some dependencies on external libraries such as `asyncio`, `re`, and `pydantic`.
🔬 The file includes a test case that can be run if the file is executed directly.
📝 Overall, this file provides a reusable action for crawling folders and filtering out certain files and directories.


### `insert_content_into_text.py`

📝 This file contains a Python class called `InsertContentIntoText` that is an implementation of a specific action. 
🔍 The purpose of this action is to insert content into a string at a specified delimiter. 
🔧 It is designed to handle cases where the delimiter occurs only once or multiple times in the string. 
📥 The inputs to this action include the existing content of the string, the delimiter, and the content to be inserted. 
💼 The output of this action is the updated content of the string after the insertion. 
🧪 The file includes two examples of how to use this action, one with no delimiters and one with two delimiters. 
🔬 The `run` method of the `InsertContentIntoText` class is responsible for executing the action. 
⚙️ The `insert_tag_content_into_string` method is a helper function used by the action to perform the insertion. 
📚 The file also imports necessary modules and defines some data models for input and output structures. 
🧪 Lastly, the file includes a test setup to manually run the action and validate its functionality.


### `prompt.py`

📝 This file contains code for generating a string using OpenAI's GPT-3 language model. 
📦 It defines the `Inputs` and `Outputs` data models for the prompt generation process.
🔍 The `trim_context` function trims the context entries to fit within the specified maximum token length.
🔧 The `build_prompt_and_instructions` function constructs the prompt and instructions based on the provided inputs.
📲 The `invoke_openai` function makes an API call to OpenAI to generate the string based on the prompt and instructions.
💾 The generated string is cached to avoid making duplicate API calls.
🏃 The `run` function orchestrates the prompt generation process, including cache retrieval and storing the result.
🍎 The `if __name__ == "__main__"` block demonstrates an example usage of the `PromptString` action.
🔬 The `run_action_manually` function is used to manually run the action with the provided inputs.
🍉 The file serves as an entry point for generating prompt-based strings using OpenAI's GPT-3 model.


### `read_file.py`

📝 This file contains a Python class called `ReadFile` that represents an action to read the contents of a file. 
🔍 It has methods for loading Jupyter notebooks and ensuring file existence. 
📄 The `run` method reads the contents of a file and returns them along with a success flag. 
🔒 If specified, it can also ensure that the file exists before reading it. 
📂 The file also includes a test case to manually run the action and remove the test file afterwards. 
💡 The purpose of this file is to provide a reusable action for reading file contents in a Python project.


### `set_issue_title.py`

📝 This file defines a class named "SetIssueTitle" which is an action to set the title of an issue.
🔑 The class extends a generic "Action" class and provides an implementation for the "run" method.
🔗 The "run" method takes an instance of the "Inputs" class as input and sets the title of an issue using the provided value.
💡 The "Inputs" class defines a single attribute named "title" of type string.
🧩 The "SetIssueTitle" class has a class variable named "id" which can be used to identify this specific action.
📚 The class uses the "pydantic" library for data validation and modeling.
🔧 The "run" method is asynchronous and calls a method named "set_title" on a "publish_service" object.
🙌 The purpose of this file is to provide a reusable action to set the title of an issue, which can be used in an automated workflow or system.
⚙️ This file may be part of a larger project or library that implements various actions for managing issues.


### `utils`

This folder contains two files. The `__init__.py` file is empty. The `prompt_context.py` file is a Python module that handles prompt context and configuration transformation. It defines classes and functions related to prompt context entries, prompt context, and prompt context configuration. The file also includes utility functions for calculating string lengths and imports external libraries. Overall, this folder is part of a larger codebase and is responsible for managing prompt context and its configuration.


### `write_into_file.py`

💡 This file contains a Python script that defines an action called "WriteIntoFile".
📝 The purpose of this action is to write content into a file.
📁 The action takes three inputs: the filepath of the file, the content to insert, and a flag indicating whether to append the content at the end of the file or replace the entire file content.
✍️ When the action is run, it opens the file and writes the content based on the provided inputs.
✅ The action returns an output indicating whether the file was written to successfully.
🔧 The action can be manually tested by running it with sample inputs.
🚮 After running the action, the test file is removed.


<!-- Living README Summary -->
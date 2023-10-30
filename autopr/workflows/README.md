

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files related to managing and organizing workflows. The `__init__.py` file contains functions for loading and collecting workflows from YAML files. The `api_git_history.yaml` file defines steps for making API calls, saving responses, and pushing to a Git repository. The `autogenerate_readmes.yaml` file contains workflows for generating and updating README summaries. The `insert_into_readme.yaml` file defines an action for inserting content into a file. The `list_and_publish_todos.yaml` file automates the process of managing and updating TODOs as GitHub issues. The `summarize_pr.yaml` file summarizes changes in a pull request.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/__init__.py)

📝 This file contains a Python script that defines functions related to loading and collecting workflows from YAML files.  
📂 It imports various modules and defines a logger.  
📥 The `_collect_workflows` function is responsible for parsing a YAML file and adding its contents to an existing workflow configuration.  
📂 The `_load_workflows_in_folder` function recursively loads all YAML files in a given folder and its subfolders, using the `_collect_workflows` function.  
🔍 The `get_all_workflows` function loads default workflows from the current directory and any test workflows specified in `_test_workflow_paths`.  
⚙️ The script also includes a block of code that is executed when the script is run directly, printing the result of `get_all_workflows`.  
🗄️ The script relies on external modules such as `pydantic` and `yaml` for parsing and validation.  
🚫 Error handling is implemented for file loading and workflow validation.  
📜 The script serves as a utility for managing and organizing workflows in a larger system.  
💻 The code can be used as a starting point for extending workflow functionality or building workflow management tools.      


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/api_git_history.yaml)

💡 This file defines a series of steps for making an API call, saving the response to a file, and committing and pushing the file to a Git repository.  
💡 The file is structured using a YAML format.  
💡 The file specifies the inputs required for the API call, such as the endpoint URL, headers, and file path.  
💡 The API call is made using the "make_api_call" action, which performs a GET request.  
💡 The response content is then saved to a file using the "write_into_file" action.  
💡 The "commit_and_push" action is used to commit and push the file to a Git repository, with a customizable commit message.  
💡 The file paths and other values can be provided as variables using the "var" keyword.  
💡 The file can be used as a template for automating API calls and version control.  
💡 The file can be customized by modifying the inputs, actions, and templates.  
💡 If the file is empty, there are no defined steps or actions.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/autogenerate_readmes.yaml)

💡 This file contains a set of workflows for generating and updating README summaries for files and folders. It includes the following functionalities:  
       
     - Summarizing a file by prompting the user to provide a summary of its contents  
     - Summarizing a folder by iterating through its files and folders and generating summaries for each  
     - Reformatting the summary results into a standardized format  
     - Inserting the formatted summary into the README file of the folder  
     - Committing and pushing the changes to the repository  
       
     If the file is empty, it will be marked as such in the summary.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines an insert_into_readme action that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
📄 The output is the content of the file after the insertion.  
🔍 The steps involve reading the file, inserting the content between the comments, and writing the updated file.  
💡 If the file doesn't exist, it will be created.  
📑 If there are no existing comments, the content will be appended to the end of the file.  
🧩 The file uses variables to reference inputs and outputs in the steps.  
🖋️ The content is inserted using HTML-style comments <!-- tag --> as delimiters.  
📝 The purpose of this file is to define a reusable action for inserting content into a file.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/list_and_publish_todos.yaml)

✏️ This file is a configuration file for a workflow called "Update TODO issues".  
✏️ The workflow is designed to list TODOs in code files and create GitHub issues for each TODO.  
✏️ It takes inputs such as the programming language and the keywords to search for (e.g., "TODO", "FIXME").  
✏️ The workflow consists of several steps, including finding and iterating through the TODOs, and building and publishing the issues.  
✏️ A "build_and_publish_todo" workflow is called for each TODO to prompt for task difficulty, description, and other details.  
✏️ The "publish_todo_issues" workflow is the main workflow that lists the TODOs and commits and pushes the prompt cache.  
✏️ The file uses YAML syntax to define the workflows, inputs, outputs, and steps.  
✏️ It also includes templates for generating issue titles, fingerprints, and issue bodies.  
✏️ The file is structured and organized, making it easy to understand and modify the workflow logic.  
✏️ The purpose of this file is to automate the process of managing and updating TODOs as GitHub issues.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/03521e243e018b61236da467e94d47d89783b5e6/./autopr/workflows/summarize_pr.yaml)

📋 This file defines a workflow called "summarize_pr" for summarizing changes in a pull request.  
⌨️ It uses a bash action to get the diff of the changes in the pull request.  
💬 Then it prompts the user to summarize the changes using markdown and emojis.  
💡 The user is instructed to provide line items with emojis to highlight the contents of the changes.  
💻 The resulting summary is stored in the "summary" variable.  
💬 Finally, the summary is posted as a comment.  

<!-- Living README Summary -->
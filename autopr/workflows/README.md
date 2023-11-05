

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python scripts and YAML configuration files for managing and automating workflows. The scripts and configurations are designed to handle tasks such as collecting and loading workflow configurations from YAML files, making API calls and committing changes to a git repository, generating summaries for files and folders, inserting content into files, finding and publishing TODOs in code, and summarizing changes in a pull request. These files provide a flexible and customizable way to automate various workflow processes.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/__init__.py)

📝 This file contains a Python script.  
🛠️ The purpose of the script is to collect and load workflow configurations from YAML files.  
📂 It recursively searches for YAML files in a specified folder and its subfolders.  
📝 The collected workflows are stored in a `TopLevelWorkflowConfig` object.  
⚠️ It handles exceptions and logs errors if there are any issues with loading or validating the workflows.  
🔄 It can also load additional test workflows if provided.  
📥 The loaded workflows are returned as the result of the `get_all_workflows()` function.  
📥 The script can be run as a standalone program to print the loaded workflows.  
📂 The script relies on other modules and classes imported at the beginning of the file.  
🚀 The script can be extended or modified to fit specific workflow configuration needs.  


### [`api_git_history.yaml`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file contains a YAML configuration for a set of workflows that summarize files and folders. It includes steps to read file contents, prompt for summaries, generate folder summaries, reformat the results, and update a README file with the summaries.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/list_and_publish_todos.yaml)

📋 This file is a configuration file for a workflow system.  
🔍 It defines a workflow called "list_todos" for finding and publishing TODOs in code.  
🔀 The workflow has steps for finding todos, checking if there are any todos, and iterating through each todo to build and publish a corresponding issue.  
📝 The workflow "build_and_publish_todo" handles the logic for creating and publishing an issue for each todo.  
🗃️ The "publish_todo_issues" workflow is responsible for updating the TODO issues.  
📑 The file also includes input and output definitions for each workflow.  
💡 The file uses various actions like "choice", "prompt", and "set_vars" to prompt for user input and perform operations.  
🚀 The goal of this file is to automate the process of finding and managing TODOs in code repositories.  
🔧 It provides a flexible and customizable way to handle different types of TODOs and publish them as issues.  


### [`summarize_pr.yaml`](https://github.com/irgolic/AutoPR/blob/551bf9c940dc6e3e8e133ab31d31d51f02ae26bf/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
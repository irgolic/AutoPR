

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python scripts and YAML configuration files for managing various workflows. The scripts are designed to collect and load workflow configurations from YAML files, handle exceptions and log errors, and perform operations such as making API calls, generating summaries of files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. The files are well-documented and can be extended or modified to fit specific workflow configuration needs.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file contains a YAML configuration for generating executive summaries of files and folders.   
📂 It defines several workflows for reading files, summarizing their contents, and generating formatted summaries.   
🗂️ The `generate_summary` workflow is the entry point for summarizing both files and folders.   
📄 The `summarize_file` workflow reads a file, prompts for a summary, and outputs the summary, URL, and reformatted file path.   
📁 The `summarize_folder` workflow summarizes each file/folder in a given folder and prompts for a folder summary.   
🔀 The `reformat_results` workflow formats the summary results into a Markdown template.   
✏️ The `insert_into_readme` workflow inserts the formatted summary into the README file.   
💾 The `commit_and_push` action commits and pushes the changes to the repository.   
📝 If a file is empty, it is assigned an "EMPTY_FILE_SUMMARY" message.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/list_and_publish_todos.yaml)

📋 This file defines a workflow for managing TODO issues in code repositories.  
🔍 It provides a way to list all TODOs in the codebase and their associated issue numbers.  
📝 The workflow includes steps for finding TODOs, prompting for task difficulty and description, and publishing issues.  
🚀 The main workflow is called "publish_todo_issues" which updates the TODO issues in the repository.  
💡 It uses a "list_todos" sub-workflow to find and iterate through each TODO.  
📂 The file also includes a sub-workflow called "build_and_publish_todo" for creating and publishing individual TODO issues.  
💻 The workflow is written in a YAML-like syntax and includes inputs, outputs, and steps.  
🔧 It uses various actions like "set_vars", "choice", and "prompt" to perform different tasks.  
🏷️ TODOs are associated with issue labels based on their difficulty level.  
📝 The file is well-documented with comments explaining the purpose of each step.  


### [`summarize_pr.yaml`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
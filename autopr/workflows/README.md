

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python scripts and YAML files that define various workflows. The scripts are responsible for loading and validating workflow configurations from YAML files, while the YAML files define different tasks and actions to be performed. These tasks include making API calls, summarizing files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. The workflows can be customized and extended to fit specific needs, and the changes made by the workflows can be committed and pushed to a git repository.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file contains a set of workflows and actions for summarizing files and folders in a directory.  
📂 The main workflows include "summarize_file" and "summarize_folder" which read and summarize files and folders, respectively.  
🗂️ The "generate_summary" workflow is the entry point for summarizing both files and folders.  
📄 The "reformat_results" workflow is used to format the summary results into a README file.  
📑 The "insert_into_readme" workflow inserts the formatted summary into the README file.  
🔄 The "generate_readme_summaries" workflow executes the other workflows to generate summaries for all the folders in the current directory.  
📝 If a file is empty, it will be marked as such in the summary.  
📂 If a folder is empty, it will not have a summary.  
🚀 The changes made by the workflows are committed and pushed to the repository.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file defines a workflow for managing TODO issues in code repositories.    
📝 It includes steps for finding TODOs, iterating over them, and publishing issues.    
🔍 The workflow prompts for task difficulty and suggestions before creating an issue.    
🗂 The file also includes a workflow to update existing TODO issues.    
🔧 It uses various inputs and outputs to customize the workflow.    
📋 The file contains a list of TODOs, each with a task and locations.    
🛠 Steps include actions like choice, prompt, set_vars, and publish_issue.    
🏷 Labels are assigned to issues based on task difficulty.    
🔄 The workflow can be customized with language and todo_keywords inputs.    
🚀 Overall, this file automates the process of managing and updating TODO issues in code repositories.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
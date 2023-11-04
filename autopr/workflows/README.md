

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of configuration files for different workflows. These workflows include tasks such as making API calls and committing changes to a git repository, generating summaries for files and folders, inserting content into files, finding and publishing TODOs in code repositories, and summarizing changes in pull requests. Each file describes the steps and inputs required to execute the respective workflow. These configurations can be used as a guide for implementing and customizing the workflows to fit specific needs.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/autogenerate_readmes.yaml)

📄 This file contains a YAML configuration for a workflow that generates summaries for files and folders in a repository.   
📝 The `summarize_file` workflow reads a file, prompts the user to provide a summary, and outputs the summary along with other file details.   
📂 The `summarize_folder` workflow summarizes each file and folder within a given folder, prompts the user for a folder summary, and generates a formatted summary for the folder.   
📑 The `reformat_results` workflow takes the folder summary and file summaries and formats them into a README template.   
📝 The `generate_summary` workflow is the entry point for summarizing both files and folders.   
📝 The `generate_readme_summaries` workflow executes the `generate_summary` workflow on the current directory to generate summaries for all files and folders.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/list_and_publish_todos.yaml)

📋 The file is a configuration file for a workflow called "Update TODO issues".   
🔍 It defines a series of steps to find and publish TODOs in code repositories.   
📝 The workflow takes inputs such as language and todo keywords, and outputs a list of issue numbers.   
🔧 It uses actions like finding todos, iterating through them, and publishing issues.   
💡 The "build_and_publish_todo" step prompts for task difficulty and issue description.   
📌 It also sets variables for issue title, body, and labels.   
📥 The "publish_todo_issues" workflow calls the "list_todos" workflow and outputs the issue number list.   
🐍 The default language is Python and the default todo keywords are "TODO" and "FIXME".   
📄 The file is written in YAML format.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/6a6b91a8d27e70df76c86d75bbf8a3bfd45ab203/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
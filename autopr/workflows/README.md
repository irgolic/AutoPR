

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files that define workflows for various tasks. These tasks include collecting and loading workflow configurations from YAML files, making API calls and committing changes to a git repository, summarizing files and folders and generating README summaries, inserting content into files, managing and publishing TODO issues, and summarizing changes in a pull request. Each file provides a description of its purpose and the steps involved in the workflow it defines. The files can be extended or modified to fit specific needs and rely on other modules and classes imported at the beginning of each file.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file contains a set of workflows for summarizing files and folders and generating a README summary.    
💼 The main workflows are `summarize_file` and `summarize_folder`, which read a file or crawl a folder respectively and generate a summary.    
📂 The `generate_summary` workflow is the entry point for summarizing both files and folders.    
🌳 The `reformat_results` workflow formats the summary results in a specific template.    
📝 The `insert_into_readme` workflow inserts the formatted summary into the README file.    
💻 The `commit_and_push` action commits and pushes the changes to the repository.    
🔍 The `list_folder` action lists the contents of a folder, excluding specified files.    
🗂️ The `generate_readme_summaries` workflow executes the defined workflows to generate README summaries.    
📄 The file also includes variables and templates for prompts and instructions.    
📂 If a folder is empty or only contains ignored files, the summary will be empty.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file contains a workflow for managing and publishing TODO issues.  
🔄 The workflow includes steps for finding TODOs, prompting for task difficulty and suggestions, and publishing issues.  
📝 The file defines inputs such as language and todo keywords, and outputs issue numbers.  
🔀 It uses conditional logic to handle cases where there are no todos.  
🔁 It iterates over todos and calls a separate workflow to build and publish each todo as an issue.  
📌 The build and publish workflow prompts for task difficulty and suggestions, and creates an issue with labels.  
📋 The file also includes a separate workflow for updating existing TODO issues.  
🧩 The workflows use various actions such as choice selection, prompting, and publishing issues.  
🛠️ The purpose of this file is to automate the process of managing and updating TODO issues in code repositories.  


### [`summarize_pr.yaml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
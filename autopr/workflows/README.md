

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of YAML files that define different workflows. These workflows automate various tasks such as making API calls, generating summaries for files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. The files provide configuration and steps for executing these workflows, allowing for customization and automation of these tasks.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/autogenerate_readmes.yaml)

📋 This file contains a YAML configuration for a workflow that summarizes files and folders.   
📁 The workflow includes steps to read and summarize a file, summarize a folder, and reformat the summary results.   
📝 It prompts the user to provide a summary for the file and folder.   
📄 The results are then written into a README file and committed to a repository.   
🗂️ The workflow can also handle empty files and folders.   
📚 The purpose of this file is to automate the process of generating living summaries for files and folders in a project.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file defines a workflow for managing TODO issues in code repositories.   
📝 It uses a series of steps to find TODOs, prompt for task difficulty and suggestions, and publish issues.   
🔍 The workflow can be customized with inputs such as language and todo keywords.   
📥 The workflow outputs a list of issue numbers for the created issues.   
📋 The file also includes a separate workflow for updating existing TODO issues.   
🚀 The purpose of this file is to automate the process of managing and resolving TODOs in code.  


### [`summarize_pr.yaml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python scripts and YAML files that serve various purposes. The `__init__.py` script collects and loads workflow configurations from YAML files, handling exceptions and logging errors. The YAML files define workflows for tasks such as making API calls, summarizing files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. These files provide reusable functionality that can be customized and extended to fit specific workflow configuration needs.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file contains a set of workflows and actions for summarizing files and folders.   
📁 The main workflows are "summarize_file" and "summarize_folder", which read file contents and generate summaries respectively.   
🗂️ The "generate_summary" workflow is the entry point for summarizing both files and folders.   
📄 The "reformat_results" workflow is responsible for formatting the summary results.   
📚 The "insert_into_readme" workflow inserts the formatted summary into a README file.   
📝 The "generate_readme_summaries" workflow executes the necessary workflows to generate summaries for the folders.   
💻 The file also includes various actions and variables for handling file operations.   
📝 If a file is empty, it will be indicated as such in the summary.   
📂 Folders are summarized by iterating through the files and folders within them and generating individual summaries.   
🚀 The changes made to the README file are then committed and pushed.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file defines a workflow for managing TODO issues in code repositories.  
🔍 The workflow has two main steps: "list_todos" and "publish_todo_issues".  
📝 The "list_todos" step finds all TODOs in the code and stores them in a variable called "todos".  
📌 The "publish_todo_issues" step iterates over the "todos" and creates GitHub issues for each TODO.  
📊 The workflow collects information about the TODOs, such as task difficulty and issue labels.  
🚀 The created issues are published on GitHub with the appropriate title, body, and labels.  
📑 The workflow also keeps track of the issue numbers and stores them in a variable called "issue_number_list".  
🔄 The "publish_todo_issues" step is part of a larger workflow called "Update TODO issues".  
📚 The purpose of this file is to automate the management and publishing of TODO issues in code repositories.  
🔧 The file can be customized by modifying the inputs and outputs of the defined steps.  


### [`summarize_pr.yaml`](https://github.com/irgolic/AutoPR/blob/50cfaeeaaedc4a6529b5a363ba237dce1404ad03/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
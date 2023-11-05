

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of YAML configuration files that define various workflows. These workflows include tasks such as collecting and loading workflow configurations from YAML files, making API calls and saving responses to files, generating summaries of files and folders, inserting content into files, listing and updating TODO issues in code, and summarizing changes in pull requests. These workflows can be run as standalone programs or integrated into other systems to automate and streamline various tasks.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/autogenerate_readmes.yaml)

📄 This file contains a YAML configuration for generating executive summaries of files and folders.  
🔍 It defines multiple workflows for reading files, summarizing their contents, and generating formatted summaries.  
📂 The `generate_summary` workflow is the entry point for summarizing both files and folders.  
🗂️ The `summarize_file` workflow reads a file, prompts for a summary, and outputs the summary and URL.  
📝 The `summarize_folder` workflow summarizes the files and folders within a folder, prompts for a folder summary, and generates a formatted summary.  
📝 The `reformat_results` workflow formats the summary and inserts it into a README file.  
⚙️ The `generate_readme_summaries` workflow executes the `generate_summary` workflow for the current directory.  
📄 The `README.md` file is automatically updated with the generated summaries.  
❌ If a file is empty, it is given a default "This file is empty" summary.  
📂 If a folder is empty, it is given an empty summary.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/list_and_publish_todos.yaml)

📝 This file is a configuration file for a workflow called "Update TODO issues".  
📋 The workflow is designed to list TODOs in code and update their corresponding issues.  
🔍 It takes inputs such as the programming language and todo keywords to filter the TODOs.  
🔄 The workflow includes steps to find the TODOs, iterate over them, and build and publish the corresponding issues.  
✅ It uses actions like "choice" and "prompt" to gather information from the user.  
📥 The workflow receives inputs like the TODO task and existing issue number, and outputs the issue number for each TODO.  
💡 It also provides prompts for suggestions on resolving the TODOs.  
📌 The resulting issues are published with titles, bodies, labels, and other relevant information.  
🔁 The workflow can be triggered by the "publish_todo_issues" step.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/a560a99ccc9a894499fe44852bcd0df209be923c/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
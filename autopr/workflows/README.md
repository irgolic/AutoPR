

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a Python script (`__init__.py`) that collects and loads workflow configurations from YAML files. The script recursively searches for YAML files in a specified folder and its subfolders. It handles exceptions and logs errors during the loading and validation process. The loaded workflows are returned as the result of the `get_all_workflows()` function. The folder also includes several YAML files that define different workflows for tasks such as making API calls and saving responses to files, automating the process of summarizing files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests.


### [`__init__.py`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/autogenerate_readmes.yaml)

📝 This file defines a series of workflows for summarizing files and folders and generating a living README summary.  
📁 The file contains several workflows, including "summarize_file", "summarize_folder", and "generate_summary".  
📑 The workflows take inputs such as file paths and folder paths, and produce outputs such as summaries, URLs, and reformatted path names.  
🧩 The workflows use actions such as reading files, prompting for user input, and committing and pushing changes.  
📚 The "reformat_results" workflow reformats the summary results and writes them into a README file.  
🗂️ The "summarize_folder" workflow iterates over files and folders in a given folder, summarizes them, and generates a summary for the folder itself.  
❓ The "generate_summary" workflow is the entry point for summarizing both files and folders.  
📜 The "generate_readme_summaries" workflow executes the "generate_summary" workflow for the current folder to generate a living README summary.  
🚀 The file is designed to automate the process of summarizing files and folders, making it easier to maintain an up-to-date README summary.  


### [`insert_into_readme.yaml`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file defines a workflow for managing TODO issues in code repositories.  


### [`summarize_pr.yaml`](https://github.com/irgolic/autopr/blob/6eca175af1a796cf6de44b15fa4a9cb81752e58c/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
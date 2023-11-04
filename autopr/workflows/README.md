

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of YAML files that define various workflows and tasks. The files outline different automation processes, such as making API calls, generating summaries of files and folders, inserting content into files, managing TODO issues in code repositories, and summarizing changes in pull requests. These workflows can be executed using a workflow management system to automate and streamline these tasks. The files provide clear instructions and configurations for each workflow, allowing for customization and extension to fit specific needs.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/autogenerate_readmes.yaml)

📄 This file contains a YAML configuration for generating living summaries of files and folders within a given directory.  
📝 The `summarize_file` workflow reads a file, prompts the user for a summary, and outputs the summary along with the file's URL and reformatted path name.  
📂 The `summarize_folder` workflow summarizes each file and folder within a given folder, prompts the user for a folder summary, and outputs the folder summary.  
🔄 The `reformat_results` workflow takes the output of `summarize_folder` and formats it into a Markdown template for the README file.  
📝 The `generate_summary` workflow acts as an entry point for summarizing both files and folders, calling either `summarize_file` or `summarize_folder` based on the input path.  
📝 The `generate_readme_summaries` workflow executes the `generate_summary` workflow for the current directory and commits the results to the repository.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file contains a workflow definition for managing TODO issues in code repositories.  
🔄 The workflow consists of several steps that involve finding TODOs, prompting for task difficulty and descriptions, and publishing the issues.  
🔍 The initial step is to list all the TODOs based on language and keywords.  
📝 Each TODO is then processed individually, with the option to assign a difficulty level and provide suggestions for resolving it.  
📌 The issues are published with labels and stored in a list.  
🔄 The workflow is triggered by a separate workflow called "publish_todo_issues".  
📊 The output of the workflow is a list of issue numbers.  
💡 The purpose of this file is to automate the management of TODO issues and facilitate collaboration in resolving them.  
🔒 The file also includes a step to commit and push the prompt cache.  
⚙️ The file is written in a YAML-like syntax and can be executed using a workflow management system.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/58930ae93625b5c6df53ea36ba4305031b0615d6/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
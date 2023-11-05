

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of files related to workflow configurations. The `__init__.py` script is used to collect and load workflow configurations from YAML files. It can recursively search for YAML files in a specified folder and its subfolders, handle exceptions, and log errors. The other YAML files define different workflows, such as making API calls, generating README summaries, inserting content into files, updating TODO issues, and summarizing pull requests. These workflows define specific steps and inputs to perform various tasks related to code management and documentation.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/__init__.py)

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


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/api_git_history.yaml)

📝 This file defines a set of steps for making an API call, saving the response to a file, and committing and pushing the file to a git repository.  
🔗 The API call endpoint URL, headers, and filepath are defined as inputs.  
🔀 The file uses a "make_api_call" action to make a GET request to the specified endpoint URL, using the provided headers.  
📄 The response content is then saved into a file specified by the filepath input, overwriting any existing content in the file.  
📦 Finally, the file is committed and pushed to a git repository, with a commit message template that includes the endpoint URL and filepath.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/autogenerate_readmes.yaml)

💡 This file contains a set of workflows for summarizing files and folders, generating README summaries, and committing and pushing the changes. It includes steps to read files, prompt for file summaries, summarize folders, format results, and insert the formatted summary into a README file. The main workflow is "generate_readme_summaries".  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines a task called "insert_into_readme" that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
💾 The task reads the file, inserts the content between the specified comments, and then writes the modified content back into the file.  
📥 If the file does not exist, it will be created.  
📑 If only one comment is found, the content will be appended to the end of the file.  
🖋️ The task uses three actions: "read_file" to read the file, "insert_content_into_text" to insert the content, and "write_into_file" to write the modified content.  
📄 The output of the task is the content of the file after the insertion.  
✅ The task returns a success flag indicating whether the write operation was successful.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/list_and_publish_todos.yaml)

📝 This file is a configuration file for a workflow called "Update TODO issues".  
🛠️ The workflow updates TODO issues in code based on certain criteria.  
📋 The workflow consists of several steps, each with specific inputs and outputs.  
🔍 The first step is to find TODOs in the code.  
✅ If no TODOs are found, an empty list is set as the issue number list.  
🔁 If TODOs are found, each TODO is iterated over to build and publish a corresponding issue.  
📝 The build_and_publish_todo step prompts for task difficulty and suggestions for resolving the TODO.  
📝 The issue title and body are generated based on the TODO information and user input.  
📝 The issue is then published with the generated title, body, and associated labels.  
🔄 The publish_todo_issues workflow calls the list_todos workflow to update the TODO issues.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/1595b4c1b1ad54f2c8501d83388e6b3d77ea6e12/./autopr/workflows/summarize_pr.yaml)

📝 This file defines a workflow called `summarize_pr` that summarizes the changes in a pull request.  
🔍 It uses the `git diff` command to get the difference between the base commit and the pull request.  
💬 It prompts the user to summarize the changes using markdown and emojis to highlight the contents of the changes.  
💡 The user's input is stored in the `summary` variable.  
💬 The summarized changes are then posted as a comment.  

<!-- Living README Summary -->
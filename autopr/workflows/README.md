

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains a collection of Python scripts and YAML files that define workflows for various tasks. The scripts are focused on loading and managing workflows from YAML files, while the YAML files define specific workflows for tasks such as making API calls, generating README summaries, inserting content into files, managing TODO issues, and summarizing changes in pull requests. These files can be used as templates or starting points for automating and organizing tasks in a larger system.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/__init__.py)

📝 This file contains a Python script that defines functions related to loading and collecting workflows from YAML files.  
📂 It imports various modules and defines a logger.  
📥 The `_collect_workflows` function is responsible for parsing a YAML file and adding its contents to an existing workflow configuration.  
📂 The `_load_workflows_in_folder` function recursively loads all YAML files in a given folder and its subfolders, using the `_collect_workflows` function.  
🔍 The `get_all_workflows` function loads default workflows from the current directory and any test workflows specified in `_test_workflow_paths`.  
⚙️ The script also includes a block of code that is executed when the script is run directly, printing the result of `get_all_workflows`.  
🗄️ The script relies on external modules such as `pydantic` and `yaml` for parsing and validation.  
🚫 Error handling is implemented for file loading and workflow validation.  
📜 The script serves as a utility for managing and organizing workflows in a larger system.  
💻 The code can be used as a starting point for extending workflow functionality or building workflow management tools.      


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/api_git_history.yaml)

💡 This file defines a series of steps for making an API call, saving the response to a file, and committing and pushing the file to a Git repository.  
💡 The file is structured using a YAML format.  
💡 The file specifies the inputs required for the API call, such as the endpoint URL, headers, and file path.  
💡 The API call is made using the "make_api_call" action, which performs a GET request.  
💡 The response content is then saved to a file using the "write_into_file" action.  
💡 The "commit_and_push" action is used to commit and push the file to a Git repository, with a customizable commit message.  
💡 The file paths and other values can be provided as variables using the "var" keyword.  
💡 The file can be used as a template for automating API calls and version control.  
💡 The file can be customized by modifying the inputs, actions, and templates.  
💡 If the file is empty, there are no defined steps or actions.  


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/autogenerate_readmes.yaml)

💡 This file contains a set of workflows for generating and updating README summaries for files and folders. It includes the following functionalities:  
       
     - Summarizing a file by prompting the user to provide a summary of its contents  
     - Summarizing a folder by iterating through its files and folders and generating summaries for each  
     - Reformatting the summary results into a standardized format  
     - Inserting the formatted summary into the README file of the folder  
     - Committing and pushing the changes to the repository  
       
     If the file is empty, it will be marked as such in the summary.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines an insert_into_readme action that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
📄 The output is the content of the file after the insertion.  
🔍 The steps involve reading the file, inserting the content between the comments, and writing the updated file.  
💡 If the file doesn't exist, it will be created.  
📑 If there are no existing comments, the content will be appended to the end of the file.  
🧩 The file uses variables to reference inputs and outputs in the steps.  
🖋️ The content is inserted using HTML-style comments <!-- tag --> as delimiters.  
📝 The purpose of this file is to define a reusable action for inserting content into a file.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file defines a workflow for managing TODO issues in code repositories.  
📝 The workflow includes steps for finding TODOs, prompting for task difficulty and description, and publishing issues.  
🔍 The workflow starts with the "list_todos" step, which takes inputs for language and todo keywords.  
🔀 If no TODOs are found, an empty list is set as the issue number list.  
🔁 If TODOs are found, the workflow iterates over each TODO and invokes the "build_and_publish_todo" step.  
📝 The "build_and_publish_todo" step prompts for task difficulty and description, sets variables, and publishes the issue.  
📋 The "publish_todo_issues" workflow lists TODOs and commits the prompt cache.  
🔚 The file ends with a commit and push action for the prompt cache.  
⚠️ The file does not contain any imports or external dependencies.  
⚠️ The file does not include any error handling or exception handling logic.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/9a54ad799cb587a621438758f92727a2e337a718/./autopr/workflows/summarize_pr.yaml)

📋 This file defines a workflow called "summarize_pr" for summarizing changes in a pull request.  
⌨️ It uses a bash action to get the diff of the changes in the pull request.  
💬 Then it prompts the user to summarize the changes using markdown and emojis.  
💡 The user is instructed to provide line items with emojis to highlight the contents of the changes.  
💻 The resulting summary is stored in the "summary" variable.  
💬 Finally, the summary is posted as a comment.  

<!-- Living README Summary -->
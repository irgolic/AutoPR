

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python scripts and YAML files for managing and automating various workflows. The `__init__.py` script defines functions for collecting and loading workflows from YAML files in a specified folder and its subfolders. The YAML files define different workflows, such as making API calls, generating README summaries, inserting content into files, updating TODO issues, and summarizing changes in pull requests. These workflows can be customized and executed to automate various tasks in a project.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/__init__.py)

📝 This file is a Python script that defines functions for collecting and loading workflows from YAML files in a specified folder and its subfolders.  
📂 It imports various modules and defines a class and functions related to workflow configuration and execution.  
📄 The main function, `get_all_workflows()`, loads default workflows from a specified folder and also allows for the loading of test workflows.  
📥 The workflow configurations are parsed from YAML files using the `pydantic` library.  
🌐 The loaded workflows are stored in a `TopLevelWorkflowConfig` object, which is a data model defined in another module.  
🔁 The `_collect_workflows()` function is used to collect and validate individual workflow configurations.  
📁 The `_load_workflows_in_folder()` function recursively loads workflows from YAML files in a specified folder and its subfolders.  
⚠️ Error handling is included for invalid workflow configurations and duplicate workflow IDs.  
🖨️ When executed as a standalone script, the `get_all_workflows()` function is called and the loaded workflows are printed.  


### [`api_git_history.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/api_git_history.yaml)

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


### [`autogenerate_readmes.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/autogenerate_readmes.yaml)

💡 This file contains a set of workflows for generating and updating README summaries for files and folders. It includes the following functionalities:  
       
     - Summarizing a file by prompting the user to provide a summary of its contents  
     - Summarizing a folder by iterating through its files and folders and generating summaries for each  
     - Reformatting the summary results into a standardized format  
     - Inserting the formatted summary into the README file of the folder  
     - Committing and pushing the changes to the repository  
       
     If the file is empty, it will be marked as such in the summary.  


### [`insert_into_readme.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/insert_into_readme.yaml)

📝 This file defines an insert_into_readme action that inserts content into a file between two HTML-style comments.  
📂 The file path, tag name, and content to insert are specified as inputs.  
📄 The output is the content of the file after the insertion.  
🔍 The steps involve reading the file, inserting the content between the comments, and writing the updated file.  
💡 If the file doesn't exist, it will be created.  
📑 If there are no existing comments, the content will be appended to the end of the file.  
🧩 The file uses variables to reference inputs and outputs in the steps.  
🖋️ The content is inserted using HTML-style comments <!-- tag --> as delimiters.  
📝 The purpose of this file is to define a reusable action for inserting content into a file.  


### [`list_and_publish_todos.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/list_and_publish_todos.yaml)

📄 This file contains a workflow for updating TODO issues.   
🔍 It lists TODOs based on specified language and keywords.   
🔄 It then iterates through each TODO and prompts for task difficulty and suggestions.   
📝 It creates an issue with the TODO details, suggestions, and labels.   
📌 The issue number is stored in a list for further use.   
💡 The workflow can be triggered with default language and keywords.   
📝 The file includes several actions and prompts for user input.   
📚 It uses templates to generate issue title, fingerprint, and body.   
🚀 The workflow publishes the created issues.  


### [`summarize_pr.yaml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/workflows/summarize_pr.yaml)

📋 This file defines a workflow called "summarize_pr" for summarizing changes in a pull request.  
⌨️ It uses a bash action to get the diff of the changes in the pull request.  
💬 Then it prompts the user to summarize the changes using markdown and emojis.  
💡 The user is instructed to provide line items with emojis to highlight the contents of the changes.  
💻 The resulting summary is stored in the "summary" variable.  
💬 Finally, the summary is posted as a comment.  

<!-- Living README Summary -->
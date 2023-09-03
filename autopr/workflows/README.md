

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python scripts and YAML files for loading and collecting workflows. The `__init__.py` file defines functions for loading workflows from YAML files in a folder and its subfolders, and the `get_all_workflows` function is the entry point. The `autogenerate_readmes.yaml` file contains workflows for summarizing files and folders in a directory and generating README summaries. The `insert_into_readme.yaml` file defines a task for inserting content into a file with optional tag-based delimiters. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request.


### `__init__.py`

📋 This file contains a Python script that defines functions related to loading and collecting workflows from YAML files.
📁 It imports necessary modules and defines a logger.
🔍 The main functions are `_collect_workflows` and `_load_workflows_in_folder`, which recursively collect workflows from YAML files in a folder and its subfolders.
🔧 The `get_all_workflows` function is the entry point, which loads default workflows and custom workflows from specified paths.
📃 The script also includes a test to print all the loaded workflows.
🔄 The purpose of this file is to provide a way to load and gather workflow configurations for further processing.


### `autogenerate_readmes.yaml`

📄 This file contains a set of workflows for summarizing files and folders in a directory.
📝 It includes steps for reading file contents, prompting for summaries, and generating README summaries.
📂 The workflows can handle both individual files and folders, summarizing their contents and generating formatted summaries.
📑 The formatted summaries are then inserted into the README file of each folder.
🔍 The file also includes a workflow for generating summaries of all the folders in the current directory.
🔄 The generated summaries can be committed and pushed to a repository.
📝 The file provides prompts and instructions for writing the file and folder summaries.
📚 It uses variables and lambda functions to dynamically generate the summaries and file paths.
⚙️ The file also includes actions for crawling folders, committing and pushing changes, and reading and writing files.
📂 If a folder is empty or contains only ignored files, the summary will be empty.


### `insert_into_readme.yaml`

📝 The file defines a task called "insert_into_readme" for inserting content into a file.
📄 The task requires three inputs: filepath, tag, and content.
🔍 It reads the contents of the file specified by the filepath input.
✏️ The task then inserts the content between HTML-style comments using the tag as a delimiter.
📝 The modified content is stored in the "content" output.
💾 Finally, the modified content is written back into the file specified by the filepath input.
📝 The "append_at_the_end" input determines whether the content should be appended to the end of the file if no delimiter is found.
📝 The task does not currently have any outputs defined.
📝 The purpose of this file is to define the steps for inserting content into a file with optional tag-based delimiters.


### `summarize_pr.yaml`

📋 This file defines a workflow called "summarize_pr" for summarizing changes in a pull request.
⌨️ It uses a bash action to get the diff of the changes in the pull request.
💬 Then it prompts the user to summarize the changes using markdown and emojis.
💡 The user is instructed to provide line items with emojis to highlight the contents of the changes.
💻 The resulting summary is stored in the "summary" variable.
💬 Finally, the summary is posted as a comment.


<!-- Living README Summary -->
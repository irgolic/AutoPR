

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python scripts and YAML files related to loading and collecting workflows. The `__init__.py` script defines functions for loading workflows from YAML files. The `autogenerate_readmes.yaml` file contains workflows and actions for generating summaries of files and folders. The `insert_into_readme.yaml` file defines a task for inserting content into a file. The `summarize_pr.yaml` file defines a workflow for summarizing changes in a pull request. Overall, the purpose of this folder is to provide a way to load and gather workflow configurations and perform various operations related to file handling and summarization.


### `__init__.py`

📋 This file contains a Python script that defines functions related to loading and collecting workflows from YAML files.
📁 It imports necessary modules and defines a logger.
🔍 The main functions are `_collect_workflows` and `_load_workflows_in_folder`, which recursively collect workflows from YAML files in a folder and its subfolders.
🔧 The `get_all_workflows` function is the entry point, which loads default workflows and custom workflows from specified paths.
📃 The script also includes a test to print all the loaded workflows.
🔄 The purpose of this file is to provide a way to load and gather workflow configurations for further processing.


### `autogenerate_readmes.yaml`

📝 The file contains a set of workflows and actions for generating summaries of files and folders.
🗂️ The main workflows are `summarize_file`, `summarize_folder`, and `generate_summary`.
📂 `summarize_file` reads a file, prompts the user to summarize its contents, and outputs the summary.
📁 `summarize_folder` summarizes each file/folder in a given folder and prompts the user to summarize the entire folder.
🌳 `generate_summary` is the entry point for summarizing both files and folders.
✨ `reformat_results` formats the results of the summarization workflows into a standardized format.
📝 `insert_into_readme` inserts the formatted summary into a README file.
🔁 `generate_readme_summaries` executes the defined workflows to generate summaries for the current folder and commits the changes.
💻 The file also contains various helper actions and steps for handling file operations and prompts.


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
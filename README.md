<div align="center">

# 🌳 AutoPR 🌳

[![Discord](https://badgen.net/badge/icon/discord?icon=nope&label&color=purple)](https://discord.gg/ykk7Znt3K6)
[![Docs](https://badgen.net/badge/icon/docs?icon=docs&label&color=blue)](https://docs.autopr.com)

Breathe life into your codebase, configurably  

</div>

## 🌟 Features

📄 Summarize changes by adding a "summarize" label to a PR  
🌳 Living summaries of your code in nested READMEs

... more coming soon!

## 🚀 Getting Started

Please see the [installation guide](https://docs.autopr.com/installing/github).

## 🐞 Known Bugs

We're pre-alpha, so expect bugs. Here are some known ones:

- Caching is not working properly, so living summaries get regenerated on every push.

See below for an example of AutoPR's README summary:

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various files and folders related to automation tasks. It includes a Dockerfile for setting up the project environment, a license file outlining the permissions and rights for the software, a Makefile for running different tasks in the project, an action.yml file defining the configuration for an automated pull request action, and several other files related to workflow configurations, data models, and schema definitions. Overall, this folder provides reusable components and configurations for automating different tasks.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./Dockerfile/)

🔧 Install git from bullseye-backports  
📝 Set up entrypoint  
📥 Copy pyproject.toml and poetry.lock  
📥 Copy the entire project  
🔧 Install project dependencies using poetry  
🏃‍♀️ Run the app using entrypoint.sh as the command


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./LICENSE.md/)

📄 This file contains the MIT License for software developed by Raphael Francis Ltd.
🔒 The license grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell the software.
📝 The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software.
🔧 The software is provided "as is" without warranty of any kind.
📚 The license is designed to protect the rights of the authors and copyright holders.



### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./Makefile/)

📝 This file defines several targets for a Python project    
🎯 `type` target runs static type checking using Pyright    
🧪 `test` target runs unit tests using pytest    
📋 `schema` target runs a command to generate schema for the project    
🔀 `all` target combines type, test, and schema targets    
🔧 The purpose of this file is to provide a convenient way to run different tasks in the project    
🐍 The file may be used as a Makefile or a task runner for the project    
💡 It is recommended to read the documentation or comments in the file for more details    
✅ The file is easy to understand and modify    
💻 This file is an important part of the project's build and development process


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./action.yml/)

📋 This file defines the configuration for an "Automatic Pull Request" action. 
🔧 It specifies the details of how the action should run, including using Docker and the Docker image to use.
🎨 It also defines the branding for the action, including the icon and color to use.
🔑 The file outlines the required inputs for the action, such as the GitHub token and base branch.
🔄 It provides default values for optional inputs, such as the loading GIF URL and target branch name template.
✍️ Additionally, it includes a flag to control whether to overwrite existing branches and pull requests.



### [`autopr`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/)

This folder contains a collection of Python files and folders that serve different purposes for automation tasks. The "actions" folder contains files that define various actions and utilities for automation, such as running commands, publishing comments, and committing changes. The "models" folder contains files that define models, actions, and configurations for a workflow automation system. The "services" folder contains files that provide services for managing actions, caching, commits, platforms, and workflows. The "workflows" folder contains scripts and files related to workflow configurations. Overall, this folder provides reusable components and configurations for automating different tasks.


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./entrypoint.sh/)

📝 This file is a shell script.
🔧 It sets the global configuration for Git.
📧 It sets the email address for the Git user.
👤 It sets the name for the Git user.
📁 It sets the safe directory for Git.
🔌 It activates a virtual environment.
🐍 It runs a Python module called autopr.gh_actions_entrypoint.


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./poetry.lock/)

📄 This file is intended to serve as an executive summary.
🔍 It provides a high-level overview of the contents of the document.
📑 The purpose of this file is to give a concise understanding of the document's main points.
🧐 It is designed for someone seeing the document for the first time.
👀 It highlights the key objectives and outcomes.
💡 It does not explain trivial details or imports.
📝 It is brief, especially if the file is empty.
💼 It helps the reader quickly grasp the document's purpose.
📊 It provides a snapshot of the document's contents.
📝 It serves as a guide for further exploration of the document.


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./pyproject.toml/)

📋 This file is a configuration file for a Python project using Poetry as a dependency management tool. 
📦 It specifies the project name, version, authors, license, and packages to include.
🔧 It defines the dependencies required for the project, including Python version and various libraries.
🔬 There is a separate section for test dependencies.
🛠️ The file also includes configuration for the build system and Pyright, a static type checker for Python.



### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./strict_workflow_schema.json/)

📋 This file contains a JSON schema definition for a strict workflow model. The purpose of this file is to define the structure and properties of a workflow, including the steps and actions involved in the workflow. The schema includes definitions for various types of actions, such as commenting, crawling folders, executing bash commands, and more. It also defines the structure of the workflow, including inputs, outputs, and steps.


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./trigger_schema.json/)

📝 This file contains a JSON schema definition.
🔍 The purpose of the file is to define the structure and properties of various data models used in a system.
🏷️ The file includes definitions for different types of actions, triggers, and parameters.
📂 Each definition includes properties such as title, description, type, and required fields.
📝 The file also includes references to other definitions within the schema.
🌟 The schema provides a standardized format for validating and manipulating data within the system.
🔧 It can be used by developers to ensure consistency and correctness when working with the defined data models.
💡 The file can serve as a documentation resource for understanding the structure and properties of the different data models.
🤖 The schema can be used by automated tools to generate code, perform data validation, or provide autocomplete suggestions.
⚠️ It's important to review and understand the definitions in this file in order to correctly use and interact with the data models in the system.


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./workflow_schema.json/)

📋 This file contains a JSON object describing a workflow definition.
📝 The workflow definition includes various types of actions that can be performed.
🔀 Actions can be performed iteratively or conditionally based on certain criteria.
🔀 Actions can include commenting, setting issue titles, crawling folders, executing bash commands, committing and pushing files, and more.
🔄 The workflow definition also includes steps which specify the order and flow of the actions.
🔧 Inputs and outputs can be defined for the workflow and individual actions.
🔀 The workflow definition allows for nesting of actions and conditionals, creating more complex workflows.
📚 The file also includes definitions for various types of declarations and models used within the workflow definition.
🗂️ The purpose of this file is to define and configure a workflow that can be executed programmatically.

<!-- Living README Summary -->
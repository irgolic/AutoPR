<div align="center">

# 🌳 AutoPR 🌳

[![Discord](https://badgen.net/badge/icon/discord?icon=nope&label&color=purple)](https://discord.gg/ykk7Znt3K6)
[![Docs](https://badgen.net/badge/icon/docs?icon=docs&label&color=blue)](https://docs.autopr.com)

Breathe life into your codebase, configurably  

</div>

## 🌟 Features

🌳 Living summaries of your code in nested READMEs
📄 Summarize changes by adding a "summarize" label to a PR  


... more coming soon!

## 🚀 Getting Started

Please see the [installation guide](https://docs.autopr.com/installing/github).

---

Below is an example of AutoPR's Living README:

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various files and directories related to a Python project. The "Dockerfile" is used to set up the project's environment and run the application. The "LICENSE.md" file contains the software's MIT License, which grants permission to use, modify, and distribute the software. The "Makefile" provides targets for running tasks in the project. The "action.yml" file defines the configuration for an automation action. The "autopr" directory contains Python files and directories for an automation system. The "entrypoint.sh" file is a shell script that sets up Git and runs the application. The "poetry.lock" and "pyproject.toml" files define the project's dependencies and configuration. The "strict_workflow_schema.json", "trigger_schema.json", and "workflow_schema.json" files provide structured definitions for creating and validating workflows.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./Dockerfile)

🔧 Install git from bullseye-backports    
📝 Set up entrypoint    
📥 Copy pyproject.toml and poetry.lock    
📥 Copy the entire project    
🔧 Install project dependencies using poetry    
🏃‍♀️ Run the app using entrypoint.sh as the command  


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./LICENSE.md)

📄 This file contains the MIT License for software developed by Raphael Francis Ltd.  
🔒 The license grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell the software.  
📝 The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software.  
🔧 The software is provided "as is" without warranty of any kind.  
📚 The license is designed to protect the rights of the authors and copyright holders.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./Makefile)

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


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./action.yml)

📋 This file defines the configuration for an "Automatic Pull Request" action.   
🔧 It specifies the details of how the action should run, including using Docker and the Docker image to use.  
🎨 It also defines the branding for the action, including the icon and color to use.  
🔑 The file outlines the required inputs for the action, such as the GitHub token and base branch.  
🔄 It provides default values for optional inputs, such as the loading GIF URL and target branch name template.  
✍️ Additionally, it includes a flag to control whether to overwrite existing branches and pull requests.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr)

This folder contains a collection of Python files and directories that serve different purposes. The "actions" directory provides reusable components for building automation and AI-related tasks. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file configures logging. The "main.py" file is the main entry point for running the autopr application. The "models" directory provides data models for an automation system. The "services" directory provides various services for managing and automating tasks within the AutoPR system. The "triggers.py" file provides a convenient way to retrieve and process trigger configurations. The "workflows" directory contains scripts and files for managing and automating workflows.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./entrypoint.sh)

📝 This file is a shell script.  
🔧 It sets the global configuration for Git.  
📧 It sets the email address for the Git user.  
👤 It sets the name for the Git user.  
📁 It sets the safe directory for Git.  
🔌 It activates a virtual environment.  
🐍 It runs a Python module called autopr.gh_actions_entrypoint.  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./pyproject.toml)

📝 This file is a configuration file for a Python project.  
📦 It uses the Poetry package manager.  
🔍 The file specifies the project name, version, description, authors, and license.  
📚 It includes a README file and defines the packages to be included in the project.  
📌 The file lists the dependencies required by the project, including Python version and various libraries.  
🔧 It also specifies test dependencies and exclusion/inclusion patterns for tooling.  
🛠️ The file defines the build system and the backend used.  
🚫 Exclusion and inclusion patterns are set for the Pyright static type checker.  
💼 The file provides a high-level overview of the project's setup and dependencies.  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./strict_workflow_schema.json)

📋 This file contains a JSON schema definition for a strict workflow model.  
📝 The schema defines various action models and iterable action models.  
🔍 Each action model represents a specific action that can be performed in a workflow.  
🔄 Iterable action models allow for iterating over a list of items and performing the action for each item.  
🔧 The schema also includes definitions for parameters, declarations, and contexts used in the actions.  
🧩 The strict workflow model includes a series of steps, each consisting of an action or iterable action.  
🌟 The purpose of this schema is to provide a structured definition for creating and validating strict workflows.  
💡 It can be used as a guide for creating workflow models and ensuring their adherence to a specific format.  
🚀 The schema allows for the creation of complex workflows by combining different action models and iterating over lists of items.  
📖 Overall, this file serves as a blueprint for building and executing strict workflows in a structured manner.  


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./trigger_schema.json)

📄 This file contains a JSON schema for a trigger configuration.  
🔗 The schema defines various trigger types such as label, comment, push, and cron triggers.  
🔀 Each trigger type has its own properties and sub-properties.  
📝 The schema also includes definitions for different action models such as commenting, crawling folders, making API calls, etc.  
🔄 The action models have their own properties and sub-properties.  
📅 The schema can be used to validate and configure triggers for automated workflows.  
🧩 The purpose of this file is to provide a standardized format for defining triggers and actions in a workflow.  
🔧 It helps developers and workflow designers to easily understand and configure triggers and actions.  
📚 The schema can be used as a reference to ensure that the trigger configuration is valid and follows the defined structure.  
🛠️ It allows for the creation of complex workflows by combining different triggers and actions.  


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./workflow_schema.json)

📄 This file is a JSON representation of a workflow definition.  
🔑 It contains various definitions for different types of actions and declarations.  
🔗 The definitions are organized under the "definitions" key.  
📝 Each definition contains information such as title, description, type, and properties.  
🔄 The workflow definition itself is represented by the "WorkflowDefinition" key.  
📝 It includes information about the name, description, inputs, outputs, and steps of the workflow.  
🔗 The steps can be a combination of actions, invocations, and conditional statements.  
🔁 Iterations are also supported through iterable action models.  
⚙️ The file provides a comprehensive structure for defining and executing workflows.  

<!-- Living README Summary -->
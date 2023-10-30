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

This folder contains various files and folders related to a project called "autopr." The files include a Dockerfile for building a Docker image, a license file specifying the MIT license, a Makefile with commands for formatting, testing, and running the project, an action configuration file for GitHub Actions, and configuration files for the project itself. The folders contain Python code and configuration files for the autonomous agent system, including actions, services, models, and workflows. Overall, this folder represents a project for automating workflows and managing actions using Python and Docker.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./Dockerfile)

🔧 Install git from bullseye-backports    
📝 Set up entrypoint    
📥 Copy pyproject.toml and poetry.lock    
📥 Copy the entire project    
🔧 Install project dependencies using poetry    
🏃‍♀️ Run the app using entrypoint.sh as the command  


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./LICENSE.md)

📄 This file contains the MIT License for software developed by Raphael Francis Ltd.  
🔒 The license grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell the software.  
📝 The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software.  
🔧 The software is provided "as is" without warranty of any kind.  
📚 The license is designed to protect the rights of the authors and copyright holders.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./Makefile)

📋 The file defines a set of commands and their dependencies.       
🔧 The `format` command runs the `black` code formatter on the project.       
📝 The `type` command runs the `pyright` static type checker on the project.       
🧪 The `test` command runs the `pytest` test suite for the `autopr` module.       
🔧 The `schema` command runs the `python` interpreter with the `autopr.models.config.entrypoints` module.       
🚀 The `all` command runs all the commands in the specified order.       


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./action.yml)

📋 This file defines the configuration for an "Automatic Pull Request" action.   
🔧 It specifies the details of how the action should run, including using Docker and the Docker image to use.  
🎨 It also defines the branding for the action, including the icon and color to use.  
🔑 The file outlines the required inputs for the action, such as the GitHub token and base branch.  
🔄 It provides default values for optional inputs, such as the loading GIF URL and target branch name template.  
✍️ Additionally, it includes a flag to control whether to overwrite existing branches and pull requests.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./autopr)

This folder contains a collection of Python files and folders that make up an autonomous agent system. The "actions" folder contains files that define various actions and utilities for the system, such as running commands, making API calls, and generating prompts. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow. The "log_config.py" file configures logging. The "main.py" file coordinates services and executes triggers based on events. The "models" folder contains code and configuration files for a larger codebase. The "services" folder provides various services for managing actions, interacting with platforms, and executing workflows. The "triggers.py" file retrieves and processes trigger configurations. The "workflows" folder contains code and YAML files for automating workflows.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./entrypoint.sh)

📝 This file is a shell script.  
🔧 It sets the global configuration for Git.  
📧 It sets the email address for the Git user.  
👤 It sets the name for the Git user.  
📁 It sets the safe directory for Git.  
🔌 It activates a virtual environment.  
🐍 It runs a Python module called autopr.gh_actions_entrypoint.  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./pyproject.toml)

📝 The file is a configuration file for the project "autopr"  
📦 It uses Poetry as the package manager for the project  
🔑 The project is licensed under the MIT license  
📚 The file specifies the dependencies required for the project, including Python, Pydantic, GitPython, and more  
🧪 There is a separate group for test dependencies, which includes Pytest and Aioresponses  
🛠️ There is a separate group for development dependencies, which includes Black  
🔧 The file also includes configuration settings for Pyright and Black  
🔒 The "build-system" section specifies the requirements for building the project  
🗒️ The "tool.black" section sets the line length and target version for the Black formatter  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./strict_workflow_schema.json)

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


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./trigger_schema.json)

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


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/f1b76ab07179745f86f1a281cdd821dd0c455e90/./workflow_schema.json)

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
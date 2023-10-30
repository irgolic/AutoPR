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

This folder contains files and folders related to an autonomous agent system. The Dockerfile sets up the environment for running the system. The LICENSE.md file provides the MIT License for the software. The Makefile defines commands for formatting, type checking, testing, and running the system. The action.yml file configures an "Automatic Pull Request" action. The autopr/ folder contains Python files and folders for various components of the system. The entrypoint.sh file sets up Git configuration and runs the system. The poetry.lock and pyproject.toml files specify project dependencies and settings. The strict_workflow_schema.json, trigger_schema.json, and workflow_schema.json files define models and schemas for workflows and triggers.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./Dockerfile)

🔧 Install git from bullseye-backports    
📝 Set up entrypoint    
📥 Copy pyproject.toml and poetry.lock    
📥 Copy the entire project    
🔧 Install project dependencies using poetry    
🏃‍♀️ Run the app using entrypoint.sh as the command  


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./LICENSE.md)

📄 This file contains the MIT License for software developed by Raphael Francis Ltd.  
🔒 The license grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell the software.  
📝 The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software.  
🔧 The software is provided "as is" without warranty of any kind.  
📚 The license is designed to protect the rights of the authors and copyright holders.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./Makefile)

📋 The file defines a set of commands and their dependencies.       
🔧 The `format` command runs the `black` code formatter on the project.       
📝 The `type` command runs the `pyright` static type checker on the project.       
🧪 The `test` command runs the `pytest` test suite for the `autopr` module.       
🔧 The `schema` command runs the `python` interpreter with the `autopr.models.config.entrypoints` module.       
🚀 The `all` command runs all the commands in the specified order.       


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./action.yml)

📋 This file defines the configuration for an "Automatic Pull Request" action.   
🔧 It specifies the details of how the action should run, including using Docker and the Docker image to use.  
🎨 It also defines the branding for the action, including the icon and color to use.  
🔑 The file outlines the required inputs for the action, such as the GitHub token and base branch.  
🔄 It provides default values for optional inputs, such as the loading GIF URL and target branch name template.  
✍️ Additionally, it includes a flag to control whether to overwrite existing branches and pull requests.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./autopr)

This folder contains a collection of Python files and folders related to an autonomous agent system. The "actions" folder contains reusable actions and utilities for common tasks in the system, such as running commands and making API calls. The "models" folder contains data models for messages, threads, issues, and pull requests. The "services" folder implements various services and functionalities for the system, such as interacting with platforms like GitHub. The "triggers" file provides a way to retrieve and process trigger configurations. The "workflows" folder contains scripts and YAML files for managing and organizing workflows. Overall, this folder provides the necessary components for automating and managing tasks in an autonomous agent system.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./entrypoint.sh)

📝 This file is a shell script.  
🔧 It sets the global configuration for Git.  
📧 It sets the email address for the Git user.  
👤 It sets the name for the Git user.  
📁 It sets the safe directory for Git.  
🔌 It activates a virtual environment.  
🐍 It runs a Python module called autopr.gh_actions_entrypoint.  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./pyproject.toml)

📝 The file is a configuration file for the project "autopr"  
📦 It uses Poetry as the package manager for the project  
🔑 The project is licensed under the MIT license  
📚 The file specifies the dependencies required for the project, including Python, Pydantic, GitPython, and more  
🧪 There is a separate group for test dependencies, which includes Pytest and Aioresponses  
🛠️ There is a separate group for development dependencies, which includes Black  
🔧 The file also includes configuration settings for Pyright and Black  
🔒 The "build-system" section specifies the requirements for building the project  
🗒️ The "tool.black" section sets the line length and target version for the Black formatter  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./strict_workflow_schema.json)

📝 This file is a JSON schema definition for a strict workflow model.  
📋 It defines various action models and their properties.  
🔀 The action models include comment, set_issue_title, crawl_folder, make_api_call, bash, choice, commit_and_push, write_into_file, find_todos, insert_content_into_text, search, prompt, publish_issue, read_file, and more.  
🔄 The action models can be used in a sequence of steps to define a workflow.  
🛠️ The workflow can be used to automate tasks in a specific order.  
🔢 The workflow can have inputs and outputs, as well as conditional logic using if statements.  
📥 The workflow can also include other workflows or be iterated over.  
✨ The goal of this file is to provide a standardized way to define and execute workflows.  
📂 It can be used in various automation tools and platforms.  


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./trigger_schema.json)

📄 This file is a JSON schema definition for a configuration file.  
🔄 It defines various action models and workflow models that can be used in a trigger-based automation system.  
🔀 The schema includes definitions for different types of triggers, such as label triggers, comment triggers, push triggers, and cron triggers.  
🔧 Each trigger type is associated with specific action models and workflow models that can be executed when the trigger is activated.  
🌟 The file also includes definitions for different types of input and output fields that can be used in the action and workflow models.  
📝 Descriptions are provided for each model and field, explaining their purpose and usage.  
📚 The schema is structured hierarchically, with nested definitions for different types of declarations and templates.  
🔗 References are used to link to other definitions within the schema.  
🗂️ The schema is designed to be extensible, allowing for the addition of new action and workflow models.  
📋 Overall, this file serves as a blueprint for creating automation workflows and defining the behavior of triggers and actions.  


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/81ba3ea7d990d2a16a82d4b31cd41ae7c18f169d/./workflow_schema.json)

📄 This file is a JSON representation of a workflow definition.  
🔗 It contains various definitions and models for different actions that can be performed within the workflow.  
⚙️ The workflow definition includes the name, description, inputs, outputs, and a list of steps.  
🔢 Each step can be a simple action or a more complex workflow invocation.  
💼 The file also defines different types of actions such as commenting, crawling folders, making API calls, and running bash commands.  
🔄 Some actions can be iterated over a list of items.  
🔀 Conditional logic can be added using If statements or lambdas.  
📝 Templates, variables, constants, and lambdas can be used to provide dynamic values to the actions.  
🔁 The workflow can be triggered with inputs and produces outputs.  
📚 The file provides a comprehensive structure for defining and executing workflows.  

<!-- Living README Summary -->
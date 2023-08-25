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

Please see the [installation guide](https://docs.autopr.com/docs/installation).

## 🐞 Known Bugs

We're pre-alpha, so expect bugs. Here are some known ones:

- Caching is not working properly, so living summaries get regenerated on every push.

See below for an example of AutoPR's README summary:

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files related to an automated workflow system. It includes a Dockerfile for setting up a Docker image, a Makefile for defining tasks and configurations, an action.yml file for configuring an Automatic Pull Request workflow, and several other files for managing the workflow, defining models and services, and configuring triggers. The code is well-documented and follows a modular and object-oriented design, making it easy to understand and extend. The folder also contains YAML files that define workflows for various tasks, which can be executed as standalone programs or used as reusable tasks in larger automation processes.


### `Dockerfile`

🔧 Sets up a Docker image based on duffn/python-poetry:3.9-bullseye
📦 Installs git from the bullseye-backports repository
📝 Copies the entrypoint.sh script and makes it executable
📝 Copies pyproject.toml and poetry.lock files
🔧 Installs project dependencies using Poetry in a virtual environment
📂 Sets the working directory to /app and copies all files
🔧 Installs the app using Poetry
🚀 Executes the entrypoint.sh script as the default command when the container starts


### `LICENSE.md`

📄 This file contains the MIT License.    
📝 It grants permission to use, modify, and distribute the software.    
👤 The license is issued by Raphael Francis Ltd.    
📜 The license requires the inclusion of the copyright notice.    
💼 It allows the software to be used for any purpose, with no warranty.    
💰 Selling copies of the software is permitted.    
🔒 The license does not hold the authors or copyright holders liable.    
🔧 The software is provided "as is" and without warranty.    
📝 This license applies to all copies or substantial portions of the software.    
📝 The license is effective from 2023.


### `Makefile`

📝 This file defines a set of tasks and configurations for a Python project.   
🔧 It uses `pyright` for static type checking.   
🧪 It runs `pytest` for running tests in the `autopr/tests` directory.   
📄 It runs `python -m autopr.models.config.entrypoints` for generating a schema.   
🔀 The `all` task includes running type checking, tests, and generating the schema.   



### `action.yml`

📋 This file is a configuration file for an Automatic Pull Request workflow.
🔧 It is used to automatically generate pull requests on GitHub.
🐳 The workflow runs using Docker.
🎨 It includes branding information such as an icon and color.
🔑 It requires a GitHub token as an input.
🌐 It allows customization of the base branch, loading GIF URL, target branch name template, and whether to overwrite existing branches and pull requests.
💡 The default values are provided for some of the inputs.



### `autopr`

This folder contains various files and folders related to an automated workflow system. It includes files for defining actions and utilities, configuring logging, coordinating and executing the workflow, defining models and services, managing triggers and workflows, and defining automated tasks. The code is well-documented and follows a modular and object-oriented design, making it easy to understand and extend. The folder also contains YAML files that define workflows for various tasks, which can be executed as standalone programs or used as reusable tasks in larger automation processes.


### `entrypoint.sh`

📝 The file is a shell script.
🔧 It configures Git with a safe directory and sets the user's email and name.
🔌 It activates a virtual environment.
🐍 It runs a Python module named `autopr.gh_actions_entrypoint`.


### `poetry.lock`

📄 This file serves as an executive summary.     
📝 It provides a concise overview of a document or project.     
🔍 It highlights the main points and purpose of the file.     
👀 Useful for someone seeing the document for the first time.     
📑 It may include key findings, recommendations, or summaries.     
📊 Can be used as a standalone document or as an introduction.     
📌 Focuses on important details to give a quick understanding.     
📝 Should be clear, concise, and easy to read.     
🖊️ Avoids unnecessary technical jargon or complex explanations.     
📋 Provides a high-level view of the contents of the file.    


### `pyproject.toml`

📝 This file is a configuration file for the "autopr" project.  
📦 It manages project dependencies using Poetry.  
🔧 It specifies the required Python version and other dependencies.  
🔑 It includes the author's information and the project's license.  
📄 It specifies the README file.  
📦 It defines the packages to be included in the project.  
🧪 It specifies test dependencies and tools.  
🛠️ It defines the build system for the project.  
🔍 It configures Pyright, a static type checker, for the project.


### `strict_workflow_schema.json`

📋 This file is a JSON schema for defining a strict workflow model.
📝 It allows you to define a workflow with different types of actions and their properties.
🔗 The schema includes definitions for various types of actions such as commenting, setting issue titles, crawling folders, executing bash commands, committing and pushing changes, writing into files, and more.
📂 Each action has its own set of inputs and outputs.
🔀 The workflow can include conditional branching using if statements and lambdas.
🔄 Actions can be executed iteratively using the iterate property.
🧩 The schema also includes definitions for parameters, templates, variables, constants, and lambda expressions.
📜 The workflow can be defined as a series of steps, each consisting of an action or a set of actions.
✨ The goal of this schema is to provide a standardized way of defining and executing workflows in a strict manner.


### `trigger_schema.json`

📄 This file is a JSON schema definition.
🔍 It defines a data structure for a trigger configuration model.
🚀 The trigger configuration model is used to configure triggers for a workflow.
📋 Triggers can include actions such as commenting, setting issue titles, crawling folders, running bash commands, committing and pushing changes, and more.
📂 Each action has its own model and set of inputs and outputs.
🔀 The trigger configuration model can include multiple triggers, such as label triggers, comment triggers, and push triggers.
🔧 The configuration allows for specifying parameters and branch names for push triggers.
💡 The purpose of this file is to provide a structured way to define and configure triggers for a workflow.


### `workflow_schema.json`

📋 This file is a JSON schema that defines the structure of a workflow definition.
🔢 It contains definitions for various types of actions that can be performed in the workflow.
📝 Each action has specific inputs and outputs defined.
🔀 The workflow definition can include steps that consist of actions, conditionals, and other workflow invocations.
🔍 The schema also defines various types of declarations, such as templates, variables, constants, and lambdas.
📂 Some of the actions defined include commenting on an issue, crawling a folder, executing a bash command, and committing and pushing changes to a repository.
🔀 Conditionals can be defined using Python lambda expressions or by checking the existence of certain variables or context values.
🔄 The workflow definition can be iterated over using the "iterate" property in certain actions.
🔧 It also allows for setting variables and invoking other workflows as part of the overall workflow execution.

<!-- Living README Summary -->
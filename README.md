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

This folder contains various files related to a Python project. It includes a Dockerfile for setting up the project environment, a Makefile for running different tasks, an action.yml file for configuring a GitHub action, a shell script for running the project, and configuration files for Poetry and strict workflows. There are also files related to licensing, JSON schemas for defining triggers and workflows, and a folder containing Python files that implement automation tasks. Overall, this folder provides the necessary files and configurations for building and automating the project.


### `Dockerfile`

🔧 Install git from bullseye-backports  
📝 Set up entrypoint  
📥 Copy pyproject.toml and poetry.lock  
📥 Copy the entire project  
🔧 Install project dependencies using poetry  
🏃‍♀️ Run the app using entrypoint.sh as the command


### `LICENSE.md`

📄 This file contains the MIT License for software developed by Raphael Francis Ltd.
🔒 The license grants permission to use, copy, modify, merge, publish, distribute, sublicense, and sell the software.
📝 The license requires that the copyright notice and permission notice be included in all copies or substantial portions of the software.
🔧 The software is provided "as is" without warranty of any kind.
📚 The license is designed to protect the rights of the authors and copyright holders.



### `Makefile`

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


### `action.yml`

📋 This file defines the configuration for an "Automatic Pull Request" action. 
🔧 It specifies the details of how the action should run, including using Docker and the Docker image to use.
🎨 It also defines the branding for the action, including the icon and color to use.
🔑 The file outlines the required inputs for the action, such as the GitHub token and base branch.
🔄 It provides default values for optional inputs, such as the loading GIF URL and target branch name template.
✍️ Additionally, it includes a flag to control whether to overwrite existing branches and pull requests.



### `autopr`

This folder contains a collection of Python files and folders that implement various actions and services for an automated process. The files define classes and methods for tasks such as running commands, publishing comments, committing changes, crawling folders, generating prompts, reading and writing files, and setting issue titles. The folder also includes files for configuring logging, defining models and configurations, and handling triggers and workflows. Overall, the folder provides reusable components for building automation tasks and demonstrates the usage of libraries like pydantic, asyncio, and openai.


### `entrypoint.sh`

📝 This file is a shell script.
🔧 It sets the global configuration for Git.
📧 It sets the email address for the Git user.
👤 It sets the name for the Git user.
📁 It sets the safe directory for Git.
🔌 It activates a virtual environment.
🐍 It runs a Python module called autopr.gh_actions_entrypoint.


### `poetry.lock`

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


### `pyproject.toml`

📋 This file is a configuration file for a Python project using Poetry as a dependency management tool. 
📦 It specifies the project name, version, authors, license, and packages to include.
🔧 It defines the dependencies required for the project, including Python version and various libraries.
🔬 There is a separate section for test dependencies.
🛠️ The file also includes configuration for the build system and Pyright, a static type checker for Python.



### `strict_workflow_schema.json`

📄 This file is a JSON schema definition for a strict workflow model. 
🔖 It contains definitions for various action models and their properties. 
🚀 The purpose of this file is to provide a structured format for defining and validating workflows. 
🔧 It includes definitions for actions like commenting, crawling folders, executing bash commands, and more. 
💡 The file also defines parameters, inputs, outputs, and conditions for each action. 
📚 It supports iterable actions that can be executed multiple times with different inputs. 
🔗 Actions can be nested within each other to create complex workflows. 
🔀 Conditional branching is supported through if-else statements. 
👥 The file also defines workflow invocations and iterable workflow invocations. 
📝 Overall, this file provides a comprehensive schema for designing and executing strict workflows.


### `trigger_schema.json`

📄 This file is a JSON schema definition for a trigger configuration.
🔗 It defines various trigger types such as label, comment, push, and cron triggers.
🔀 Each trigger type has its own set of properties and sub-properties.
🔧 The schema also defines different action models that can be associated with each trigger type.
📝 The action models specify the name, description, inputs, and outputs of each action.
🔄 Some action models can be iterated over using the "iterate" property.
🔑 The schema also includes definitions for different types of declarations like template, variable, constant, and lambda declarations.
🗂️ There are also definitions for different types of inputs and outputs for actions.
📅 Overall, this file provides a comprehensive schema for defining triggers and their associated actions in a workflow system.


### `workflow_schema.json`

📝 This file is a JSON schema that defines a workflow definition for a tool or system.
🔢 It contains various definitions for different types of actions that can be performed within the workflow.
🔀 Actions include commenting, crawling folders, executing bash commands, and more.
📚 The schema also defines parameters, inputs, and outputs for each action.
📑 Workflow steps are defined as an array of actions, with the ability to nest actions within each other.
🔁 The schema allows for the definition of iterative actions that can be repeated multiple times.
🧩 Some actions have additional properties and dependencies defined within the schema.
💡 Conditional logic can be implemented using the IfLambda and IfContextNotExists definitions.
🔛 The file also defines the WorkflowDefinition object, which represents the overall structure of a workflow.
📄 Inputs, outputs, and steps are specified within the WorkflowDefinition object.

<!-- Living README Summary -->
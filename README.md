<div align="center">

<img src="website/static/img/AutoPR_Mark_color.png" alt="AutoPR logo" width=300 />

<h1>🌳 AutoPR 🌳</h1>

[![Discord](https://badgen.net/badge/icon/discord?icon=nope&label&color=purple)](https://discord.gg/ykk7Znt3K6)
[![Docs](https://badgen.net/badge/icon/docs?icon=docs&label&color=blue)](https://docs.autopr.com)

Breathe life into your codebase

</div>

## 🌟 Features

🌳 Living summaries of your code in nested READMEs   
📝 TODOs kept track of in issues  
⏳ Keep history of an API call's result in git    
📄 Summarize changes by adding a "summarize" label to a PR  
🫵 Custom actions configured in YAML

## 🚀 Getting Started

Please see the [installation guide](https://docs.autopr.com/installing/github).

---

Below is an example of AutoPR's Living README:

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various files and directories related to automating tasks in a pull request workflow. The Dockerfile sets up a Docker image and installs dependencies using Poetry. The LICENSE.md file contains the MIT License for the software. The Makefile defines targets for formatting, type checking, testing, and more. The action.yml file configures an automatic pull request workflow. The autopr directory contains Python files and directories for actions, services, workflows, and configurations. The entrypoint.sh file is a shell script that sets up Git configuration. The poetry.lock file provides an overview of the project's dependencies. The pyproject.toml file is a configuration file for the Python project. The strict_workflow_schema.json and trigger_schema.json files define schemas for strict workflows and triggers. The workflow_schema.json file defines a schema for workflow definitions.


### [`Dockerfile`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./Dockerfile)

🏗️ Sets up a Docker image based on the `duffn/python-poetry:3.9-bullseye` image    
🔧 Installs git from the bullseye-backports repository    
📥 Copies an entrypoint script and makes it executable    
📥 Copies the `pyproject.toml` and `poetry.lock` files    
🔧 Activates the virtual environment and installs the project dependencies using Poetry    
📥 Copies the rest of the files to the `/app` directory    
🔧 Installs the application using Poetry    
🚀 Sets the entrypoint to `/entrypoint.sh` for running the app    


### [`LICENSE.md`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./LICENSE.md)

📄 This file contains the MIT License.  
🔒 The license grants permission to use, modify, and distribute the software.  
📝 The license requires the copyright notice and permission notice to be included in all copies.  
🚫 The software is provided "as is" without warranty.  
📅 The license copyright has beenupdated to the year 2023.  
💼 The license is owned by Raphael Francis Ltd.  


### [`Makefile`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./Makefile)

📝 This file is a makefile-like configuration file.  
🔧 It defines various targets and their associated commands.  
💻 The targets are: `format`, `type`, `test`, `schema`, and `all`.  
🔧 The `format` target runs a command to format code using the `black` tool.  
🔧 The `type` target runs a command to perform type checking using `pyright`.  
🔧 The `test` target runs pytest on the `autopr/tests` directory.  
🔧 The `schema` target runs a command to generate configuration entrypoints using `autopr.models.config`.  
🔧 The `all` target runs all the targets in sequence: `format`, `type`, `test`, and `schema`.  
🔧 This file is meant to automate common development tasks and ensure code quality.  


### [`action.yml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./action.yml)

📄 This file is a configuration file for an automatic pull request workflow.  
🔧 It specifies the details for running the workflow, such as the Docker image to use.  
🎨 It also includes branding information, such as the icon and color to use.  
🔑 The file defines inputs required for the workflow, such as the GitHub token and base branch.  
🎥 It includes a default loading GIF URL to display while the pull request is being generated.  
🌿 The file defines a template for the name of the target branch.  
🔄 It specifies whether to overwrite existing branches and pull requests when creating from issues.  


### [`autopr/`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr)

This folder contains a collection of Python files and directories that provide various actions, services, workflows, and configurations for automating tasks in a pull request workflow. The files include actions for running commands, generating choices, publishing comments on GitHub issues, committing changes, searching for keywords, making API calls, and more. There are also files for managing logging, defining triggers and workflows, configuring services, and defining data models. The directories contain additional files for managing and running actions, defining workflows, and handling events. Overall, this folder provides a comprehensive set of tools and functionalities for automating tasks in a pull request workflow.  


### [`entrypoint.sh`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./entrypoint.sh)

📝 The file is a shell script  
🔧 It sets the Git configuration for a specific directory  
✉️ It sets the user email and name for Git commits  
📦 It activates a virtual environment  
🐍 It runs a Python module called `autopr.gh_actions_entrypoint`  


### [`poetry.lock`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./poetry.lock)

📄 This file is an executive summary  of a project or report  
🔍 It provides a high-level overview of the main points  
📝 It highlights key findings, conclusions, and recommendations  
📊 It may include a summary of data or analysis  
👥 It is intended for someone who is new to the project or report  
🚫 It does not include trivial details or technical explanations  
💡 It gives a clear understanding of the purpose and scope of the project  
👀 It provides a quick glance at the content without going into depth  
💼 It serves as a starting point for further exploration or discussion  
📌 It is concise and easy to read, even if the file is empty  


### [`pyproject.toml`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./pyproject.toml)

📋 This file is a configuration file for a Python project using Poetry.  
🔍 It contains information about the project's name, version, and authors.  
📄 The license of the project is specified as MIT.  
📦 It lists the packages and their dependencies required for the project.  
🧪 There are separate dependencies for testing and development.  
🔧 The build system used is Poetry.  
🔍 The file also includes configuration for the Pyright static type checker.  
🔍 It specifies the line length and target version for the Black code formatter.  


### [`strict_workflow_schema.json`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./strict_workflow_schema.json)

📄 The file is a JSON schema describing a strict workflow definition.  
🔍 It defines various actions that can be performed within the workflow.  
🔀 Actions include commenting, setting issue titles, walking files, making API calls, running bash commands, and more.  
📝 Each action has its own set of inputs and outputs.  
🔄 The workflow steps are defined as an array of actions.  
📚 The schema also includes definitions for various data types and declarations used within the actions.  
📝 The purpose of the file is to provide a standardized structure for defining and executing strict workflows.  
🗂️ The schema can be used to validate and ensure the correctness of workflow definitions.  
🧩 It allows for easy integration with other tools and systems that support the schema.  
📚 The file can serve as a reference for understanding the structure and capabilities of strict workflows.  


### [`trigger_schema.json`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./trigger_schema.json)

📄 This file is a JSON schema definition for a configuration file.  
🏷️ It defines various action models and trigger models.  
🔀 The action models represent different actions that can be performed in a workflow.  
🔄 The trigger models represent different triggers that can initiate a workflow.  
🔖 The schema provides a structure for defining inputs, outputs, and other properties for each action and trigger.  
📝 It also defines different types of declarations and templates that can be used within the actions and triggers.  
🔀 The "TopLevelTriggerConfig" object is the main configuration object that contains an array of triggers.  
📌 Each trigger can be of type "label", "comment", "push", or "cron".  
🌐 Overall, this file provides a standardized structure for defining workflows and their triggers and actions.  


### [`workflow_schema.json`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./workflow_schema.json)

📄 This file is a JSON schema definition for a workflow definition.  
🔧 It defines various types and properties for different actions and declarations used in the workflow.  
📝 The schema includes definitions for actions like commenting, setting issue title, walking files, making API calls, running bash commands, etc.  
📚 It also defines different types of declarations like template, variable, constant, and lambda declarations.  
📋 The workflow definition includes a name, description, inputs, and outputs.  
🔢 It consists of a list of steps which can be actions, workflow invocations, or conditional statements.  
🔀 Conditional statements can have if-else branches and support different conditions like lambda expressions and context checks.  
🔄 Workflow invocations can be either regular or iterable.  
🔑 Overall, this file provides a structured definition for creating and executing workflows with various actions and conditions.  

<!-- Living README Summary -->

<div align="center">

<img src="website/static/img/AutoPR_Mark_color.png" alt="AutoPR logo" width=300 />

<h1>🌳 AutoPR 🌳</h1>

[![Discord](https://badgen.net/badge/icon/discord?icon=nope&label&color=purple)](https://discord.gg/ykk7Znt3K6)
[![Docs](https://badgen.net/badge/icon/docs?icon=docs&label&color=blue)](https://docs.autopr.com)

Breathe life into your codebase

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

This folder contains a collection of files and folders related to an autonomous agent system. The Dockerfile sets up a Docker image for the application, while the LICENSE.md file contains the MIT License for the software. The Makefile is used to automate development tasks and ensure code quality. The action.yml file configures an automatic pull request workflow, and the autopr/ folder contains reusable actions and services for automating processes. The entrypoint.sh file is a shell script that sets up Git configuration and runs a Python module. The poetry.lock and pyproject.toml files are configuration files for a Python project using Poetry. The strict_workflow_schema.json, trigger_schema.json, and workflow_schema.json files are JSON schemas that define the structure and properties of different workflows and triggers.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./Dockerfile)

🏗️ Sets up a Docker image based on the `duffn/python-poetry:3.9-bullseye` image    
🔧 Installs git from the bullseye-backports repository    
📥 Copies an entrypoint script and makes it executable    
📥 Copies the `pyproject.toml` and `poetry.lock` files    
🔧 Activates the virtual environment and installs the project dependencies using Poetry    
📥 Copies the rest of the files to the `/app` directory    
🔧 Installs the application using Poetry    
🚀 Sets the entrypoint to `/entrypoint.sh` for running the app    


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./LICENSE.md)

📄 This file contains the MIT License.  
🔒 The license grants permission to use, modify, and distribute the software.  
📝 The license requires the copyright notice and permission notice to be included in all copies.  
🚫 The software is provided "as is" without warranty.  
📅 The license is valid until 2023.  
💼 The license is owned by Raphael Francis Ltd.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./Makefile)

📝 This file is a makefile-like configuration file.  
🔧 It defines various targets and their associated commands.  
💻 The targets are: `format`, `type`, `test`, `schema`, and `all`.  
🔧 The `format` target runs a command to format code using the `black` tool.  
🔧 The `type` target runs a command to perform type checking using `pyright`.  
🔧 The `test` target runs pytest on the `autopr/tests` directory.  
🔧 The `schema` target runs a command to generate configuration entrypoints using `autopr.models.config`.  
🔧 The `all` target runs all the targets in sequence: `format`, `type`, `test`, and `schema`.  
🔧 This file is meant to automate common development tasks and ensure code quality.  


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./action.yml)

📄 This file is a configuration file for an automatic pull request workflow.  
🔧 It specifies the details for running the workflow, such as the Docker image to use.  
🎨 It also includes branding information, such as the icon and color to use.  
🔑 The file defines inputs required for the workflow, such as the GitHub token and base branch.  
🎥 It includes a default loading GIF URL to display while the pull request is being generated.  
🌿 The file defines a template for the name of the target branch.  
🔄 It specifies whether to overwrite existing branches and pull requests when creating from issues.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./autopr)

This folder contains a collection of Python files and folders that implement various actions, services, and workflows for an autonomous agent system. The files define classes and functions for actions such as running commands, publishing comments, and committing changes. The folders contain code for managing triggers, executing workflows, and defining data models. Overall, this folder provides a range of reusable actions and services that can be used to automate processes or scripts.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./entrypoint.sh)

📝 The file is a shell script  
🔧 It sets the Git configuration for a specific directory  
✉️ It sets the user email and name for Git commits  
📦 It activates a virtual environment  
🐍 It runs a Python module called `autopr.gh_actions_entrypoint`  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./pyproject.toml)

📋 This file is a configuration file for a Python project using Poetry.  
🔍 It contains information about the project's name, version, and authors.  
📄 The license of the project is specified as MIT.  
📦 It lists the packages and their dependencies required for the project.  
🧪 There are separate dependencies for testing and development.  
🔧 The build system used is Poetry.  
🔍 The file also includes configuration for the Pyright static type checker.  
🔍 It specifies the line length and target version for the Black code formatter.  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./strict_workflow_schema.json)

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


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./trigger_schema.json)

📋 This file is a JSON schema that defines the structure and properties of various action models and trigger configurations.  
📝 It contains definitions for different types of actions, such as commenting, making API calls, walking files, and more.  
🔄 The file also includes definitions for iterable versions of these actions, which can be used in loop-like workflows.  
🕒 It defines a CronTrigger configuration for scheduling actions based on cron expressions.  
🔀 The TopLevelTriggerConfig object is the main configuration that can contain multiple triggers.  
🔗 The triggers can be label triggers, comment triggers, push triggers, or cron triggers.  
⚙️ Each trigger has its own set of properties and can be used to define custom workflows and automation tasks.  
💡 The file provides a comprehensive schema for building and configuring workflows in a structured and standardized manner.  
🛠️ It can be used as a reference to validate and generate workflows, ensuring consistency and correctness.  
📚 The file is designed to be easily extensible, allowing for the addition of new action models and trigger configurations.  


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/3bf8a4d34accd718d73d2e505656ba2ec3df1e98/./workflow_schema.json)

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
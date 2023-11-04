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

This folder contains files and folders related to a workflow automation system. The Dockerfile sets up a Docker image and installs dependencies using Poetry. The LICENSE.md file contains the MIT License for the software. The Makefile is used to automate development tasks. The action.yml file configures an automatic pull request workflow. The autopr/ folder contains Python files for implementing various functionalities of the automation system. The entrypoint.sh file sets Git configuration and runs a Python module. The poetry.lock and pyproject.toml files are configuration files for the Python project using Poetry. The strict_workflow_schema.json, trigger_schema.json, and workflow_schema.json files define the structure and properties of the workflow definitions.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./Dockerfile)

🏗️ Sets up a Docker image based on the `duffn/python-poetry:3.9-bullseye` image    
🔧 Installs git from the bullseye-backports repository    
📥 Copies an entrypoint script and makes it executable    
📥 Copies the `pyproject.toml` and `poetry.lock` files    
🔧 Activates the virtual environment and installs the project dependencies using Poetry    
📥 Copies the rest of the files to the `/app` directory    
🔧 Installs the application using Poetry    
🚀 Sets the entrypoint to `/entrypoint.sh` for running the app    


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./LICENSE.md)

📄 This file contains the MIT License.  
🔒 The license grants permission to use, modify, and distribute the software.  
📝 The license requires the copyright notice and permission notice to be included in all copies.  
🚫 The software is provided "as is" without warranty.  
📅 The license is valid until 2023.  
💼 The license is owned by Raphael Francis Ltd.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./Makefile)

📝 This file is a makefile-like configuration file.  
🔧 It defines various targets and their associated commands.  
💻 The targets are: `format`, `type`, `test`, `schema`, and `all`.  
🔧 The `format` target runs a command to format code using the `black` tool.  
🔧 The `type` target runs a command to perform type checking using `pyright`.  
🔧 The `test` target runs pytest on the `autopr/tests` directory.  
🔧 The `schema` target runs a command to generate configuration entrypoints using `autopr.models.config`.  
🔧 The `all` target runs all the targets in sequence: `format`, `type`, `test`, and `schema`.  
🔧 This file is meant to automate common development tasks and ensure code quality.  


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./action.yml)

📄 This file is a configuration file for an automatic pull request workflow.  
🔧 It specifies the details for running the workflow, such as the Docker image to use.  
🎨 It also includes branding information, such as the icon and color to use.  
🔑 The file defines inputs required for the workflow, such as the GitHub token and base branch.  
🎥 It includes a default loading GIF URL to display while the pull request is being generated.  
🌿 The file defines a template for the name of the target branch.  
🔄 It specifies whether to overwrite existing branches and pull requests when creating from issues.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr)

This folder contains a collection of Python files and folders that implement various functionalities for a workflow automation system. It includes files for managing triggers and workflows, performing actions on a GitHub repository, configuring logging settings, defining data models, and executing customizable workflows. The services folder contains classes for handling different aspects of the workflow, such as caching data, managing commits, interacting with the GitHub platform, and publishing updates to pull requests. The actions folder includes files that define classes and functions for performing specific actions, such as running commands, generating choices, and making API calls. The workflows folder contains YAML files that define different automated tasks and actions.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./entrypoint.sh)

📝 The file is a shell script  
🔧 It sets the Git configuration for a specific directory  
✉️ It sets the user email and name for Git commits  
📦 It activates a virtual environment  
🐍 It runs a Python module called `autopr.gh_actions_entrypoint`  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./pyproject.toml)

📋 This file is a configuration file for a Python project using Poetry.  
🔍 It contains information about the project's name, version, and authors.  
📄 The license of the project is specified as MIT.  
📦 It lists the packages and their dependencies required for the project.  
🧪 There are separate dependencies for testing and development.  
🔧 The build system used is Poetry.  
🔍 The file also includes configuration for the Pyright static type checker.  
🔍 It specifies the line length and target version for the Black code formatter.  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./strict_workflow_schema.json)

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


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./trigger_schema.json)

📝 The file is a JSON schema that defines the structure and properties of various trigger configurations.  
📝 It includes definitions for different types of triggers such as comment, push, label, and cron triggers.  
📝 Each trigger has its own set of properties and actions that can be performed when the trigger is activated.  
📝 The schema also includes definitions for different types of actions that can be performed, such as making API calls, executing bash commands, and interacting with files and folders.  
📝 The schema allows for the creation of complex workflows by combining different triggers and actions.  
📝 The properties of each trigger and action are defined using JSON objects with specific titles, descriptions, and types.  
📝 Some actions have additional properties that are required or have default values.  
📝 The schema also includes definitions for different types of declarations, such as template declarations, variable declarations, and constant declarations.  
📝 The schema is designed to be used as a configuration file for a workflow automation system, where triggers and actions can be defined to perform specific tasks based on certain conditions or events.  
📝 The file is organized into sections that define the different trigger configurations and their associated properties.  


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./workflow_schema.json)

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
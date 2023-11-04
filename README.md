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

This folder contains files and folders related to an autonomous agent system. The main entry point for the application is the `main.py` file, which handles triggers and workflows. The `autopr` folder contains Python files and folders that define various actions, services, and models for the system. The `Dockerfile` sets up a Docker image for the application, and the `Makefile` automates common development tasks. There are also configuration files for licensing, GitHub Actions, and workflow definitions.


### [`Dockerfile`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./Dockerfile)

🏗️ Sets up a Docker image based on the `duffn/python-poetry:3.9-bullseye` image    
🔧 Installs git from the bullseye-backports repository    
📥 Copies an entrypoint script and makes it executable    
📥 Copies the `pyproject.toml` and `poetry.lock` files    
🔧 Activates the virtual environment and installs the project dependencies using Poetry    
📥 Copies the rest of the files to the `/app` directory    
🔧 Installs the application using Poetry    
🚀 Sets the entrypoint to `/entrypoint.sh` for running the app    


### [`LICENSE.md`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./LICENSE.md)

📄 This file contains the MIT License.  
🔒 The license grants permission to use, modify, and distribute the software.  
📝 The license requires the copyright notice and permission notice to be included in all copies.  
🚫 The software is provided "as is" without warranty.  
📅 The license is valid until 2023.  
💼 The license is owned by Raphael Francis Ltd.  


### [`Makefile`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./Makefile)

📝 This file is a makefile-like configuration file.  
🔧 It defines various targets and their associated commands.  
💻 The targets are: `format`, `type`, `test`, `schema`, and `all`.  
🔧 The `format` target runs a command to format code using the `black` tool.  
🔧 The `type` target runs a command to perform type checking using `pyright`.  
🔧 The `test` target runs pytest on the `autopr/tests` directory.  
🔧 The `schema` target runs a command to generate configuration entrypoints using `autopr.models.config`.  
🔧 The `all` target runs all the targets in sequence: `format`, `type`, `test`, and `schema`.  
🔧 This file is meant to automate common development tasks and ensure code quality.  


### [`action.yml`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./action.yml)

📄 This file is a configuration file for an automatic pull request workflow.  
🔧 It specifies the details for running the workflow, such as the Docker image to use.  
🎨 It also includes branding information, such as the icon and color to use.  
🔑 The file defines inputs required for the workflow, such as the GitHub token and base branch.  
🎥 It includes a default loading GIF URL to display while the pull request is being generated.  
🌿 The file defines a template for the name of the target branch.  
🔄 It specifies whether to overwrite existing branches and pull requests when creating from issues.  


### [`autopr/`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./autopr)

This folder contains a collection of Python files and folders related to an autonomous agent system. The "actions" folder contains Python files that define various actions for the system, such as importing modules, running commands, and making API calls. The "gh_actions_entrypoint.py" file serves as the entry point for a GitHub Actions workflow, orchestrating the workflow execution and interacting with the GitHub API. The "log_config.py" file configures logging settings and creates loggers. The "main.py" file implements the main entry point for the application, handling triggers and workflows. The "models" folder contains files for defining workflows and data models. The "services" folder includes services for managing actions, interacting with the GitHub platform, and executing workflows. The "triggers.py" file retrieves trigger configurations from specified files. The "workflows" folder contains scripts and configuration files for various workflow-related tasks.  


### [`entrypoint.sh`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./entrypoint.sh)

📝 The file is a shell script  
🔧 It sets the Git configuration for a specific directory  
✉️ It sets the user email and name for Git commits  
📦 It activates a virtual environment  
🐍 It runs a Python module called `autopr.gh_actions_entrypoint`  


### [`poetry.lock`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./pyproject.toml)

📋 This file is a configuration file for a Python project using Poetry.  
🔍 It contains information about the project's name, version, and authors.  
📄 The license of the project is specified as MIT.  
📦 It lists the packages and their dependencies required for the project.  
🧪 There are separate dependencies for testing and development.  
🔧 The build system used is Poetry.  
🔍 The file also includes configuration for the Pyright static type checker.  
🔍 It specifies the line length and target version for the Black code formatter.  


### [`strict_workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./strict_workflow_schema.json)

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


### [`trigger_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./trigger_schema.json)

📄 This file is a JSON schema that defines the structure and properties of various trigger actions and models.  
🔗 It includes definitions for different types of actions such as commenting, setting issue titles, walking files, making API calls, running bash commands, and more.  
🚀 The schema also defines different workflow models that can be triggered based on labels, comments, pushes, or cron schedules.  
💡 It provides a comprehensive and flexible framework for defining and configuring automated actions and workflows.  
🔖 The file is organized into sections for each action or model, with properties such as name, description, inputs, and outputs.  
🔍 It also includes definitions for different parameter types, such as templates, variables, constants, and lambdas.  
🔄 The schema allows for iterative actions, where an action can be performed multiple times in a loop with different inputs.  
✅ Additional properties are not allowed, ensuring a strict and consistent structure for the actions and models.  
📝 The purpose of this file is to serve as a reference and guide for developers implementing automated workflows and actions within a system or application.  


### [`workflow_schema.json`](https://github.com/raphael-francis/AutoPR-internal/blob/2f0b06f314ecec7d8eddf44bf3ce5967d4ba90e1/./workflow_schema.json)

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
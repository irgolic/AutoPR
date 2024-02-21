<div align="center">

<img src="website/static/img/AutoPR_Mark_color.png" alt="AutoPR logo" width=300 />

<h1>🌳 AutoPR 🌳</h1>

[![Discord](https://badgen.net/badge/icon/discord?icon=nope&label&color=purple)](https://discord.gg/ykk7Znt3K6)
[![Docs](https://badgen.net/badge/icon/docs?icon=docs&label&color=blue)](https://docs.autopr.com)

Run AI-powered workflows over your codebase

</div>

## 🌟 Features

🌳 Living summaries of your code in nested READMEs   
📝 TODOs kept track of in issues  
⏳ Keep history of an API call's result in git    
📄 Summarize changes by adding a "summarize" label to a PR  
🫵 Custom actions configured in YAML

## 🚀 Getting Started

Please see the [installation guide](https://docs.autopr.com/installing/github).

## 📝 Maintainer Note

Though used internally, this project is currently not actively maintained.

Until v0.1.2, AutoPR autonomously generated pull requests from issues. 
There's another actively maintained open-source (AGPL) solution for this use case – [Sweep](https://github.com/sweepai/sweep).
If you'd still prefer to use AutoPR for this, set the following line in your github actions yaml:

```yaml
      uses: docker://ghcr.io/irgolic/autopr:v0.1.2
```

---

Below is an example of AutoPR's Living README:

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains files and folders related to an autonomous agent system. The Dockerfile sets up a Docker image and installs dependencies using Poetry. The LICENSE.md file contains the MIT License for the software. The Makefile is used for automating development tasks. The action.yml file configures an automatic pull request workflow. The autopr folder contains Python files and folders for the autonomous agent system. The entrypoint.sh file is a shell script that sets up Git and activates a virtual environment. The poetry.lock file provides an executive summary of the project. The pyproject.toml file is a configuration file for the Python project. The strict_workflow_schema.json file defines a strict workflow structure. The trigger_schema.json file defines trigger configurations. The workflow_schema.json file defines a workflow structure.


### [`Dockerfile`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./Dockerfile)

🏗️ Sets up a Docker image based on the `duffn/python-poetry:3.9-bullseye` image    
🔧 Installs git from the bullseye-backports repository    
📥 Copies an entrypoint script and makes it executable    
📥 Copies the `pyproject.toml` and `poetry.lock` files    
🔧 Activates the virtual environment and installs the project dependencies using Poetry    
📥 Copies the rest of the files to the `/app` directory    
🔧 Installs the application using Poetry    
🚀 Sets the entrypoint to `/entrypoint.sh` for running the app    


### [`LICENSE.md`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./LICENSE.md)

📄 This file contains the MIT License.  
🔒 The license grants permission to use, modify, and distribute the software.  
📝 The license requires the copyright notice and permission notice to be included in all copies.  
🚫 The software is provided "as is" without warranty.  
📅 The license is valid until 2023.  
💼 The license is owned by Raphael Francis Ltd.  


### [`Makefile`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./Makefile)

📝 This file is a makefile-like configuration file.  
🔧 It defines various targets and their associated commands.  
💻 The targets are: `format`, `type`, `test`, `schema`, and `all`.  
🔧 The `format` target runs a command to format code using the `black` tool.  
🔧 The `type` target runs a command to perform type checking using `pyright`.  
🔧 The `test` target runs pytest on the `autopr/tests` directory.  
🔧 The `schema` target runs a command to generate configuration entrypoints using `autopr.models.config`.  
🔧 The `all` target runs all the targets in sequence: `format`, `type`, `test`, and `schema`.  
🔧 This file is meant to automate common development tasks and ensure code quality.  


### [`action.yml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./action.yml)

📄 This file is a configuration file for an automatic pull request workflow.  
🔧 It specifies the details for running the workflow, such as the Docker image to use.  
🎨 It also includes branding information, such as the icon and color to use.  
🔑 The file defines inputs required for the workflow, such as the GitHub token and base branch.  
🎥 It includes a default loading GIF URL to display while the pull request is being generated.  
🌿 The file defines a template for the name of the target branch.  
🔄 It specifies whether to overwrite existing branches and pull requests when creating from issues.  


### [`autopr/`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./autopr)

This folder contains a collection of Python files and folders related to an autonomous agent system. The "actions" folder contains various Python files that implement different actions for the system, such as running commands, generating choices, and making API calls. The "gh_actions_entrypoint.py" file is the entry point for a GitHub Actions workflow and handles the execution of the workflow. The "log_config.py" file is used to configure logging settings. The "main.py" file serves as the main entry point for the application and handles triggers and workflows. The "models" folder contains data models for messages, issues, and pull requests. The "services" folder contains implementations of different services for a pull request workflow system. The "triggers.py" file retrieves trigger configurations from specified files. The "workflows" folder contains YAML files that define different workflows for automation.  


### [`entrypoint.sh`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./entrypoint.sh)

📝 The file is a shell script  
🔧 It sets the Git configuration for a specific directory  
✉️ It sets the user email and name for Git commits  
📦 It activates a virtual environment  
🐍 It runs a Python module called `autopr.gh_actions_entrypoint`  


### [`poetry.lock`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./poetry.lock)

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


### [`pyproject.toml`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./pyproject.toml)

📋 This file is a configuration file for a Python project using Poetry.  
🔍 It contains information about the project's name, version, and authors.  
📄 The license of the project is specified as MIT.  
📦 It lists the packages and their dependencies required for the project.  
🧪 There are separate dependencies for testing and development.  
🔧 The build system used is Poetry.  
🔍 The file also includes configuration for the Pyright static type checker.  
🔍 It specifies the line length and target version for the Black code formatter.  


### [`strict_workflow_schema.json`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./strict_workflow_schema.json)

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


### [`trigger_schema.json`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./trigger_schema.json)

📄 This file contains a JSON schema definition for a trigger configuration in a workflow.   
🔀 The `TopLevelTriggerConfig` object is the main entry point for defining triggers.  
🌟 Triggers can be of different types: `LabelTrigger`, `CommentTrigger`, `PushTrigger`, and `CronTrigger`.  
📝 Each trigger type has its own set of properties and sub-objects that define the trigger behavior.  
💡 Triggers can perform various actions such as commenting, setting issue titles, walking files, making API calls, executing bash commands, and more.  
🔁 Some trigger actions can be performed iteratively with the help of the `IterableActionModel` objects.  
📆 The `CronTrigger` type allows triggers to be scheduled based on a cron schedule.  
📚 The schema also defines several supporting objects and models used within the trigger configuration.  
👀 The `definitions` section of the schema provides detailed definitions for each object and model.  
🔒 The schema enforces additionalProperties to be false, ensuring strict adherence to the defined structure.  


### [`workflow_schema.json`](https://github.com/irgolic/AutoPR/blob/dd6cdd8d0b3a21a773a5a4308a7f2991ec105d16/./workflow_schema.json)

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

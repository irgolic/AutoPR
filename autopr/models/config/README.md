

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains various Python files that provide a framework for defining and executing workflows with customizable actions and context variables. The files define models for data validation, workflow structures, triggers, and variable transformations. They also include classes and declarations for rendering and evaluating different types of variables within a context. Overall, the folder provides a flexible and extensible system for handling workflows and variables in a Python application.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/__init__.py)

This file is empty.  


### [`common.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/common.py)

📄 This file contains two Pydantic model classes: `StrictModel` and `ExtraModel`.  
🔒 The `StrictModel` class enforces strict validation of input data, forbidding any extra fields.  
🔀 The `smart_union` attribute of `StrictModel.Config` enables smart union behavior for type validation.  
🔓 The `ExtraModel` class allows for extra fields in the input data.  
📝 These model classes are likely used to define the structure and validation rules for data in a Python application.  


### [`elements.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/elements.py)

📚 This file defines various models and classes related to workflows, actions, and context variables.  
📝 It includes models for context actions such as setting variables and conditional execution.  
🔀 It also defines models for executables, actions, choices, sequences, and workflows.  
🔧 The file dynamically builds action models based on currently defined actions.  
📄 It includes models for input and output values, as well as specifications for required inputs and outputs.  
🧩 The file also includes a top-level workflow configuration model.  
🚀 Overall, this file provides a framework for defining and executing workflows with customizable actions and context variables.  


### [`entrypoints.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/entrypoints.py)

📄 This file contains code for building workflow definitions and trigger configurations.  
🔧 It imports various modules and defines classes and functions related to workflows and triggers.  
🔀 The `build_workflows` function dynamically builds workflow models based on currently defined workflows.  
🔗 The `WorkflowInvocationConfigs` variable stores the generated workflow models.  
📝 The `TriggerModel` class and its subclasses define different types of triggers.  
📋 The `TopLevelTriggerConfig` class represents a configuration with a list of triggers.  
🔍 The `get_all_executable_ids` function retrieves all executable IDs from actions and workflows.  
📂 The `StrictExecutableId` type represents a literal union of all executable IDs.  
📝 The file also includes code for generating JSON schemas for triggers and workflows.  


### [`transform.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/transform.py)

📄 This file defines two generic classes for transforming variables between config and action types.   
🔄 The `TransformsInto` class is used to transform a config variable into the type used in the action.   
⚙️ The `TransformsFrom` class is used to define the config type for certain IO types.   
🔒 The `transform_from_config` method in the `TransformsInto` class is responsible for the transformation process.   
❌ The `transform_from_config` method is marked as `NotImplementedError` and needs to be implemented in a subclass.   
❌ The `_get_config_type` method in the `TransformsFrom` class is also marked as `NotImplementedError` and needs to be implemented in a subclass.   
📚 The file makes use of the `typing` module for type hints.   
📝 The file imports the `ContextDict` class from the `autopr.models.executable` module.   


### [`value_declarations.py`](https://github.com/irgolic/AutoPR/blob/b2b4a5bd4e292eda4c0821413a3477a310eca6b8/./autopr/models/config/value_declarations.py)

📝 This file contains code that defines various classes and declarations related to variables and parameters.  
🧩 The purpose of this file is to provide a framework for rendering and evaluating different types of variables within a context.  
💡 It includes classes for template declarations, variable declarations, constant declarations, lambda declarations, and parameter declarations.  
🔢 These classes provide methods to render their respective values within a given context.  
📋 The file also defines a `Param` class that represents a parameter passed in trigger invocation.  
🔀 The `ParamDeclaration` class allows referencing and rendering of parameters within the context.  
📚 The file also includes a `ValueDeclaration` union type that encompasses different types of value declarations.  
🔀 The `EVAL_CONTEXT` dictionary provides a predefined context for evaluating lambda expressions.  
📝 Overall, this file provides a flexible and extensible system for handling variables and parameters within a specific context.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python code for defining and executing workflows with customizable actions and context variables. The code includes models and classes for workflow structures, actions, context actions, and variable transformations. It also provides frameworks for rendering and evaluating different types of variables within a context, as well as building workflow definitions and triggers. The code uses the Pydantic library for structure and validation, and generates JSON schemas for triggers and workflows. Overall, this folder provides a comprehensive system for defining, executing, and handling workflows in a Python application.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/__init__.py)

This file is empty.  


### [`common.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/common.py)

📄 This file contains two Pydantic model classes: `StrictModel` and `ExtraModel`.  
🔒 The `StrictModel` class enforces strict validation of input data, forbidding any extra fields.  
🔀 The `smart_union` attribute of `StrictModel.Config` enables smart union behavior for type validation.  
🔓 The `ExtraModel` class allows for extra fields in the input data.  
📝 These model classes are likely used to define the structure and validation rules for data in a Python application.  


### [`elements.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/elements.py)

📚 This file defines various models and classes related to workflows, actions, and context variables.  
📝 It includes models for context actions such as setting variables and conditional execution.  
🔀 It also defines models for executables, actions, choices, sequences, and workflows.  
🔧 The file dynamically builds action models based on currently defined actions.  
📄 It includes models for input and output values, as well as specifications for required inputs and outputs.  
🧩 The file also includes a top-level workflow configuration model.  
🚀 Overall, this file provides a framework for defining and executing workflows with customizable actions and context variables.  


### [`entrypoints.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/entrypoints.py)

📄 This file contains Python code for building workflow definitions and triggers.  
🔧 The purpose of the file is to dynamically generate workflow models and schemas.  
🔄 It defines functions for building workflow models and retrieving executable IDs.  
🔀 The file also defines trigger models for different types of events.  
📝 It includes parsing entrypoints for workflow definitions and trigger configurations.  
📚 The file uses the Pydantic library for creating models and schemas.  
🔧 It generates JSON schemas for triggers and workflows.  
📂 The schemas are written to separate files: trigger_schema.json, workflow_schema.json, and strict_workflow_schema.json.  
👀 The code is executed if the file is run directly, generating the JSON schemas.  
📝 The file can be used as a reference for understanding workflow configuration and trigger setup.  


### [`transform.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/transform.py)

📄 This file defines two generic classes for transforming variables between config and action types.   
🔄 The `TransformsInto` class is used to transform a config variable into the type used in the action.   
⚙️ The `TransformsFrom` class is used to define the config type for certain IO types.   
🔒 The `transform_from_config` method in the `TransformsInto` class is responsible for the transformation process.   
❌ The `transform_from_config` method is marked as `NotImplementedError` and needs to be implemented in a subclass.   
❌ The `_get_config_type` method in the `TransformsFrom` class is also marked as `NotImplementedError` and needs to be implemented in a subclass.   
📚 The file makes use of the `typing` module for type hints.   
📝 The file imports the `ContextDict` class from the `autopr.models.executable` module.   


### [`value_declarations.py`](https://github.com/raphael-francis/AutoPR-internal/blob/096da5bd0357ff1bbe5486a2e192ca26c295a1d7/./autopr/models/config/value_declarations.py)

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
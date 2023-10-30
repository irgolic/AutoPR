

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains two files: "__init__.py" and "prompt_context.py". The "__init__.py" file is empty. The "prompt_context.py" file is used for managing and transforming prompt context in a natural language processing application. It includes classes and functions for working with prompt context entries and configurations, as well as functions for trimming the context and invoking OpenAI's Chat Completion API.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/0aabc10f58cc0543244c461caaef386a82b74854/./autopr/actions/utils/__init__.py)

This file is empty.  


### [`prompt_context.py`](https://github.com/raphael-francis/AutoPR-internal/blob/0aabc10f58cc0543244c461caaef386a82b74854/./autopr/actions/utils/prompt_context.py)

📄 This file contains code for managing and transforming prompt context in a natural language processing application.  
🔧 It includes classes and functions for working with prompt context entries and configurations.  
📝 The `PromptContext` class represents a dictionary mapping context headings to values, with methods for formatting and rendering the context.  
🔀 The `PromptContextInConfig` class represents a configuration for prompt context, with different types of declarations for variables, templates, lambdas, and constants.  
✂️ The `trim_context` function is used to trim the prompt context if it exceeds a specified maximum token length, based on a given strategy.  
📝 The `invoke_openai` function is an asynchronous function that invokes OpenAI's Chat Completion API with a prompt and instructions to generate a response.  
🔧 The file also includes various imports for dependencies and type annotations.  

<!-- Living README Summary -->
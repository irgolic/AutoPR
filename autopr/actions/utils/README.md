

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains two files. The `__init__.py` file is empty. The `prompt_context.py` file provides functionality for managing and manipulating prompt context in a conversational AI system. It defines classes and functions for representing and manipulating prompt context, trimming the context if it exceeds a specified token length, calculating the token length of a string for a given model, and invoking the OpenAI Chat Completion API. The file also includes import statements and uses external libraries such as `pydantic`, `tenacity`, and `tiktoken`.


### [`__init__.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/actions/utils/__init__.py)

This file is empty.  


### [`prompt_context.py`](https://github.com/irgolic/AutoPR/blob/1d818f4daeb78662b7d831d89a73d3258bb95e2f/./autopr/actions/utils/prompt_context.py)

📝 This file contains code for handling prompt context in a conversational AI system.  
🔢 It defines classes and functions related to the representation and manipulation of prompt context.  
📋 The `PromptContext` class represents a dictionary mapping heading strings to context variable values.  
📝 The `PromptContextInConfig` class is used to transform prompt context from a config representation to the `PromptContext` class.  
✂️ The `trim_context` function is used to trim the prompt context if it exceeds a specified token length.  
💡 The `get_string_token_length` function calculates the token length of a string for a given model.  
🔀 The `invoke_openai` function is used to invoke the OpenAI Chat Completion API.  
📝 The file also contains various import statements and type annotations.  
💡 The code uses external libraries such as `pydantic`, `tenacity`, and `tiktoken`.  
🔧 The purpose of this file is to provide functionality for managing and manipulating prompt context in a conversational AI system.  

<!-- Living README Summary -->
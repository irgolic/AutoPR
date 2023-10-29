

<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains Python code for managing prompt context in a chatbot application. The `prompt_context.py` file defines a `PromptContext` class that represents a dictionary mapping headings to context variable values. It provides methods for formatting the context as a string and calculating the token length. The file also includes declarations for prompt context in a config file and functions for trimming the context and invoking the OpenAI Chat Completion API.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/actions/utils/__init__.py)

This file is empty.  


### [`prompt_context.py`](https://github.com/raphael-francis/AutoPR-internal/blob/c479ccb445eededecd497d0d91bc86a1df0f2300/./autopr/actions/utils/prompt_context.py)

📄 This file contains Python code for a prompt context class and related declarations.  
🔄 The `PromptContext` class represents a dictionary mapping heading strings to context variable values.  
🔢 It provides methods for formatting the context as a string and calculating the token length.  
📝 The file also includes various declarations for prompt context in a config file.  
✂️ The `trim_context` function is used to trim the context based on a maximum token length and a trimming strategy.  
🔁 The `invoke_openai` function is an async function that invokes the OpenAI Chat Completion API.  
⚠️ The file includes import statements for various libraries and modules used in the code.  
🔧 The code uses type hints and annotations to specify the expected types of variables and function return values.  
🧪 The code includes some test-related imports and decorators from the `tenacity` library.  
📚 The code relies on external libraries such as `openai`, `pydantic`, and `tiktoken`.  

<!-- Living README Summary -->


<!-- Living README Summary -->
## 🌳 Living Summary

This folder contains two files: "__init__.py" and "prompt_context.py". "__init__.py" is an empty file. "prompt_context.py" is a Python file that implements a prompt context model for auto PR (pull request) generation. It includes classes and functions related to defining and transforming prompt contexts, and also defines different types of declarations for prompt context in config. The file imports modules like `pydantic`, `tiktoken`, and `jinja2` for type checking, encoding, and template rendering.


### [`__init__.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/actions/utils/__init__.py/)

This file is empty.


### [`prompt_context.py`](https://github.com/raphael-francis/AutoPR-internal/tree/main/./autopr/actions/utils/prompt_context.py/)

📄 This file contains Python code implementing a prompt context model for auto PR generation.
🔧 It includes classes and functions related to defining and transforming prompt contexts.
📝 The `PromptContext` class represents a dictionary mapping headings to context variable values.
🔢 The `PromptContextEntry` class represents a single entry in the context heading dictionary.
🧩 The file also defines different types of declarations for prompt context in config.
🔀 The `PromptContextInConfig` class transforms prompt context declarations from config into `PromptContext` instances.
🔍 The `get_string_token_length` function calculates the token length of a string based on a given model.
📝 The file includes docstrings and comments explaining the purpose and usage of the code.
🧪 The code seems to be part of a larger project related to auto PR generation and configuration.
🔧 It imports modules like `pydantic`, `tiktoken`, and `jinja2` for type checking, encoding, and template rendering.    

<!-- Living README Summary -->
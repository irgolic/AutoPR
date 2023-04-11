import tiktoken
from tiktoken import Tokenizer

_tokenizer_cache: dict[int, Tokenizer] = {}

def get_tiktoken_tokenizer(model_max_length: int):
    global _tokenizer_cache

    if model_max_length not in _tokenizer_cache:
        _tokenizer_cache[model_max_length] = Tokenizer()
    return _tokenizer_cache[model_max_length]

def get_tokenizer(model_max_length: int):
    return get_tiktoken_tokenizer(model_max_length)
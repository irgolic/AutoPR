import transformers

_tokenizer_cache: dict[int, transformers.GPT2TokenizerFast] = {}


def get_tokenizer(model_max_length: int):
    global _tokenizer_cache

    if model_max_length not in _tokenizer_cache:
        _tokenizer_cache[model_max_length] = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=model_max_length)
    return _tokenizer_cache[model_max_length]

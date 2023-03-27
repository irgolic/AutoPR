import transformers

_tokenizer = None


def get_tokenizer(model_max_length: int):
    global _tokenizer

    if _tokenizer is None:
        _tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2', model_max_length=model_max_length)
    return _tokenizer

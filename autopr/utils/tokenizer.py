from typing import Optional

import transformers

# FIXME use tiktoken instead

_cached_tokenizer = None


def get_tokenizer():
    global _cached_tokenizer

    if _cached_tokenizer is None:
        _cached_tokenizer = transformers.GPT2TokenizerFast.from_pretrained('gpt2')
    return _cached_tokenizer

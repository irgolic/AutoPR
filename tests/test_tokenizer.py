import pytest
from autopr.utils.tokenizer import get_tiktoken_tokenizer

def test_tiktoken_tokenizer_with_simple_strings():
    tokenizer = get_tiktoken_tokenizer()

    text = "This is a simple text."
    expected_token_count = 6

    token_count = tokenizer(text)
    assert token_count == expected_token_count, f"Expected {expected_token_count} tokens, got {token_count}"

def test_tiktoken_tokenizer_with_chat_messages():
    tokenizer = get_tiktoken_tokenizer()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "name": "Alice", "content": "What's the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
    ]
    expected_token_count = 38

    token_count = tokenizer(messages)
    assert token_count == expected_token_count, f"Expected {expected_token_count} tokens, got {token_count}"

if __name__ == "__main__":
    pytest.main()
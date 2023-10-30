import os


def build_mock_dict():
    prompt_to_response = {}

    mock_prompts_dir = os.path.join(
        os.path.dirname(__file__),
        "resources",
        "mock_prompts",
    )
    for folder in os.listdir(mock_prompts_dir):
        folder_path = os.path.join(mock_prompts_dir, folder)
        prompt_path = os.path.join(folder_path, "prompt.txt")
        response_path = os.path.join(folder_path, "response.txt")
        with open(prompt_path, "r") as f:
            prompt = f.read()
        with open(response_path, "r") as f:
            response = f.read()
        prompt_to_response[prompt] = response

    return prompt_to_response


prompt_to_response = build_mock_dict()


def mock_openai(messages, **kwargs):
    prompt = messages[-1]["content"]
    if prompt not in prompt_to_response:
        raise ValueError(f"Unexpected prompt: {prompt}")
    response = prompt_to_response[prompt]

    async def _():
        return {"choices": [{"message": {"content": response}}]}

    return _()

import json
from typing import Any

import pydantic


def truncate_strings(obj: Any, length: int = 100) -> Any:
    if isinstance(obj, str):
        if len(obj) < length:
            return obj
        return obj[:length] + "... (truncated)"
    elif isinstance(obj, dict):
        return {key: truncate_strings(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [truncate_strings(value) for value in obj]
    return obj


def nested_to_dict(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {key: nested_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [nested_to_dict(value) for value in obj]
    elif isinstance(obj, pydantic.BaseModel):
        return nested_to_dict(obj.dict(by_alias=True))
    return obj


def format_for_publishing(obj: Any) -> str:
    dict_obj = nested_to_dict(obj)
    if isinstance(dict_obj, dict):
        dict_obj = {
            key: value
            for key, value in dict_obj.items()
            if not (key.startswith("__") and key.endswith("__"))
        }
    truncated_dict_obj = truncate_strings(dict_obj)
    dumped_json = json.dumps(truncated_dict_obj, indent=2)
    return dumped_json

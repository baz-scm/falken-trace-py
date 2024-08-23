from __future__ import annotations

import os
from importlib.util import find_spec
from typing import Any


# method 'str.removeprefix()' was added in Python 3.9
def removeprefix(input_str: str, prefix: str) -> str:
    if input_str.startswith(prefix):
        return input_str[len(prefix) :]
    return input_str


def normalize_path(path: str, path_prefix: str) -> str:
    return removeprefix(path, path_prefix).lstrip("/")


def flatten_dict(data: dict[str, Any], parent_key: str = "") -> dict[str, str]:
    """Creates a single level dict by concatenating keys with dots and values as strings."""
    items = {}
    for key, value in data.items():
        new_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key))
        else:
            items[new_key] = str(value)
    return items


def is_dd_trace_enabled() -> bool:
    if find_spec("ddtrace") is None:
        return False

    return os.environ.get("DD_TRACE_ENABLED", "true").lower() in ("true", "1")

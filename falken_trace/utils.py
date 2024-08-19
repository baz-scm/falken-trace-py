import os
from importlib.util import find_spec


# method 'str.removeprefix()' was added in Python 3.9
def removeprefix(input_str: str, prefix: str) -> str:
    if input_str.startswith(prefix):
        return input_str[len(prefix) :]
    return input_str


def normalize_path(path: str, path_prefix: str) -> str:
    return removeprefix(path, path_prefix).lstrip("/")


def is_dd_trace_enabled() -> bool:
    if find_spec("ddtrace") is None:
        return False

    return os.environ.get("DD_TRACE_ENABLED", "true").lower() in ("true", "1")

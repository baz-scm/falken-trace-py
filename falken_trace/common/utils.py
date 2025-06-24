from __future__ import annotations

import inspect
import os
from importlib.util import find_spec
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import FrameType


def get_outer_frames(frame: FrameType | None, max_frames: int = 5) -> Iterator[inspect.FrameInfo]:
    """Get a records for a frame and all higher (calling) frames.

    Copied and adjusted version of inspect.getouterframes()
    """
    frame_count = 0
    while frame and frame_count < max_frames:
        frame_info = (frame,) + inspect.getframeinfo(frame, 0)  # noqa: RUF005
        if frame_count:  # the first frame is itself
            yield inspect.FrameInfo(*frame_info)
        frame = frame.f_back
        frame_count += 1


def normalize_path(path: str, path_prefix: str) -> str:
    return path.removeprefix(path_prefix).lstrip("/")


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

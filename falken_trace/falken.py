from __future__ import annotations

import inspect
import os
from typing import TYPE_CHECKING, Callable

from typing_extensions import ParamSpec

from .utils import removeprefix

if TYPE_CHECKING:
    from ddtrace import Span, Tracer

P = ParamSpec("P")


def wrap_dd_span(wrapped: Callable[P, Span], _instance: Tracer, args: P.args, kwargs: P.kwargs) -> Span:
    span: Span = wrapped(*args, **kwargs)

    work_dir = os.getcwd()
    for frame in inspect.stack()[1:]:  # first frame is itself
        if frame.filename.startswith(work_dir) and "site-packages" not in frame.filename:
            span.set_tag("code.filepath", removeprefix(frame.filename, work_dir))
            span.set_tag("code.lineno", str(frame.lineno))
            span.set_tag("code.parent_func", frame.function)
            break

    return span

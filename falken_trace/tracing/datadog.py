from __future__ import annotations

import inspect
import os
from typing import TYPE_CHECKING, Callable

from typing_extensions import ParamSpec

from falken_trace.config import env_vars_config
from falken_trace.utils import normalize_path

if TYPE_CHECKING:
    from ddtrace import Span, Tracer

P = ParamSpec("P")


def wrap_dd_span(wrapped: Callable[P, Span], _instance: Tracer, args: P.args, kwargs: P.kwargs) -> Span:
    span: Span = wrapped(*args, **kwargs)
    if not env_vars_config.falken_trace_enabled:
        return span

    work_dir = os.getcwd()
    for frame_info in inspect.stack()[1:]:  # first frame is itself
        if frame_info.function == "func_wrapper" and "ddtrace" in frame_info.filename:  # noqa: SIM102
            # trying to get the actual definition of the callable
            if (func := frame_info.frame.f_locals.get("f")) or (func := frame_info.frame.f_locals.get("coro")):
                file_path = inspect.getsourcefile(func) or ""
                if file_path.startswith(work_dir) and "site-packages" not in file_path:
                    _, lineno = inspect.getsourcelines(func)
                    span.set_tag("code.filepath", normalize_path(path=file_path, path_prefix=work_dir))
                    span.set_tag("code.lineno", str(lineno + 1))  # points originally to the `tracer` decorator
                    span.set_tag("code.func", func.__name__)

        if frame_info.filename.startswith(work_dir) and "site-packages" not in frame_info.filename:
            span.set_tag("code.wrap_filepath", normalize_path(path=frame_info.filename, path_prefix=work_dir))
            span.set_tag("code.wrap_lineno", str(frame_info.lineno))
            span.set_tag("code.wrap_func", frame_info.function)
            break

    return span

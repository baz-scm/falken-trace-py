from __future__ import annotations

import inspect
import os
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from typing_extensions import ParamSpec

from falken_trace.config import env_vars_config
from falken_trace.utils import flatten_dict, normalize_path, removeprefix

if TYPE_CHECKING:
    from collections.abc import Awaitable

    from ddtrace import Span

if env_vars_config.dd_trace_enabled:
    from ddtrace import tracer

T = TypeVar("T")
P = ParamSpec("P")

# an API route can be set for both sync and async functions
FUNCTION_PREFIXES = ("async def ", "def ")


async def wrap_fastapi_entrypoint_span(
    wrapped: Callable[P, Awaitable[T]], _instance: None, args: P.args, kwargs: P.kwargs
) -> T:
    if (dependant := kwargs.get("dependant")) and hasattr(dependant, "call"):
        work_dir = os.getcwd()
        file_path = inspect.getsourcefile(dependant.call) or ""
        lines, lineno = inspect.getsourcelines(dependant.call)

        # `getsourcelines()` returns the code lines with decorators, line breaks, etc.
        line: str | tuple[int, str] | None = next(
            ((i, line.lstrip()) for (i, line) in enumerate(lines) if line.lstrip().startswith(FUNCTION_PREFIXES)), None
        )
        if isinstance(line, tuple):
            lineno += line[0]
            line = line[1].split("(", maxsplit=1)[0]
            for prefix in FUNCTION_PREFIXES:
                line = removeprefix(line, prefix)

        if env_vars_config.dd_trace_enabled and (span := tracer.current_span()):
            # can be `None`, if DD is disabled or FastAPI is not patched
            span.set_tag("code.filepath", normalize_path(path=file_path, path_prefix=work_dir))
            span.set_tag("code.lineno", str(lineno))
            span.set_tag("code.func", line)

            if env_vars_config.falken_include_params and (values := kwargs.get("values")):
                attach_func_params(span=span, param_args=values)

    if inspect.iscoroutinefunction(wrapped):
        return await wrapped(*args, **kwargs)
    else:
        return wrapped(*args, **kwargs)  # type:ignore[return-value]


def attach_func_params(span: Span, param_args: dict[str, Any]) -> None:
    for param, arg in param_args.items():
        if hasattr(arg, "model_dump"):  # true, if `pydantic.BaseModel`
            flat = flatten_dict(arg.model_dump())
            for flat_key, value in flat.items():
                span.set_tag(f"params.{param}.{flat_key}", value)
        else:
            span.set_tag(f"params.{param}", arg)

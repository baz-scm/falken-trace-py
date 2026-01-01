from __future__ import annotations

import inspect
import os
from typing import TYPE_CHECKING, Any, TypeVar, cast

from typing_extensions import ParamSpec

from falken_trace.common.cache import SpanTags, get_api_path_tags, set_api_path_tags
from falken_trace.common.config import env_vars_config
from falken_trace.common.utils import flatten_dict, normalize_path

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from ddtrace.trace import Span
    from fastapi.dependencies.models import Dependant

if env_vars_config.dd_trace_enabled:
    try:
        from ddtrace.trace import tracer
    except ImportError:
        # keeping it to support lower `ddtrace` versions
        from ddtrace import tracer

T = TypeVar("T")
P = ParamSpec("P")

# an API route can be set for both sync and async functions
FUNCTION_PREFIXES = ("async def ", "def ")


async def wrap_fastapi_entrypoint_span(
    wrapped: Callable[P, Awaitable[T]],
    _instance: None,
    args: Any,  # noqa: ANN401
    kwargs: Any,  # noqa: ANN401
) -> T:
    if (dependant := kwargs.get("dependant")) and hasattr(dependant, "call"):
        api_path = dependant.path
        span_tags = get_api_path_tags(path=api_path)

        if not span_tags:
            span_tags = extract_span_tags(dependant)
            set_api_path_tags(path=api_path, tags=span_tags)

        if env_vars_config.dd_trace_enabled and (span := tracer.current_span()):
            # can be `None`, if DD is disabled or FastAPI is not patched
            span.set_tag("code.filepath", span_tags.file_path)
            span.set_tag("code.lineno", span_tags.line_number)
            span.set_tag("code.func", span_tags.func_name)

            if env_vars_config.falken_include_params and (values := kwargs.get("values")):
                attach_func_params(span=span, param_args=values)

    if inspect.iscoroutinefunction(wrapped):
        return await wrapped(*args, **kwargs)
    else:
        return wrapped(*args, **kwargs)  # type: ignore[invalid-return-type]


def extract_span_tags(dependant: Dependant) -> SpanTags:
    api_path_func = cast("Callable[..., Any]", dependant.call)  # the existence is already checked before
    work_dir = os.getcwd()
    file_path = inspect.getsourcefile(api_path_func) or ""
    lines, lineno = inspect.getsourcelines(api_path_func)

    # `getsourcelines()` returns the code lines with decorators, line breaks, etc.
    line: str | tuple[int, str] | None = next(
        ((i, line.lstrip()) for (i, line) in enumerate(lines) if line.lstrip().startswith(FUNCTION_PREFIXES)), None
    )
    if isinstance(line, tuple):
        lineno += line[0]
        line = line[1].split("(", maxsplit=1)[0]
        for prefix in FUNCTION_PREFIXES:
            line = line.removeprefix(prefix)

    return SpanTags(
        file_path=normalize_path(path=file_path, path_prefix=work_dir), line_number=str(lineno), func_name=line
    )


def attach_func_params(span: Span, param_args: dict[str, Any]) -> None:
    for param, arg in param_args.items():
        if hasattr(arg, "model_dump"):  # true, if `pydantic.BaseModel`
            flat = flatten_dict(arg.model_dump())
            for flat_key, value in flat.items():
                span.set_tag(f"params.{param}.{flat_key}", value)
        else:
            span.set_tag(f"params.{param}", arg)

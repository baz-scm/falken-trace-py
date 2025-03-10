import wrapt

from falken_trace import config
from falken_trace.tracing.datadog import wrap_dd_span
from falken_trace.web.fastapi import wrap_fastapi_entrypoint_span

if config.env_vars_config.falken_trace_enabled:
    if config.env_vars_config.dd_trace_enabled:
        try:
            wrapt.wrap_function_wrapper("ddtrace.trace", "Tracer.start_span", wrap_dd_span)
        except AttributeError:
            # fallback to v2 import
            wrapt.wrap_function_wrapper("ddtrace", "Tracer.start_span", wrap_dd_span)
    if config.env_vars_config.fastapi_installed:
        wrapt.wrap_function_wrapper("fastapi.routing", "run_endpoint_function", wrap_fastapi_entrypoint_span)

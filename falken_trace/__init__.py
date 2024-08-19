import wrapt

from falken_trace import config
from falken_trace.falken import wrap_dd_span

if config.env_vars_config.falken_trace_enabled:  # noqa: SIM102
    if config.env_vars_config.dd_trace_enabled:
        wrapt.wrap_function_wrapper("ddtrace", "Tracer.start_span", wrap_dd_span)

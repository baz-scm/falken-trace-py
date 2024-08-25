import os

from falken_trace.utils import is_dd_trace_enabled


class EnvVarsConfig:
    def __init__(self) -> None:
        self.dd_trace_enabled = is_dd_trace_enabled()
        self.falken_trace_enabled = os.environ.get("FALKEN_TRACE_ENABLED", "true").lower() in ("true", "1")
        self.falken_include_params = os.environ.get("FALKEN_INCLUDE_PARAMS", "true").lower() in ("true", "1")


env_vars_config = EnvVarsConfig()

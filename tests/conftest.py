from __future__ import annotations

from collections.abc import Generator

import pytest

from falken_trace.config import env_vars_config


@pytest.fixture
def disbale_falken_trace() -> Generator[None, None, None]:
    env_vars_config.falken_trace_enabled = False
    yield
    env_vars_config.falken_trace_enabled = True

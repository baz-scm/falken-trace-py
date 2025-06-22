from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from falken_trace.common.config import env_vars_config

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def disbale_falken_trace() -> Generator[None, None, None]:
    env_vars_config.falken_trace_enabled = False
    yield
    env_vars_config.falken_trace_enabled = True

# falken-trace-py

## Getting Started

### Requirements

- Python 3.8+
- ddtrace 2.9+

### Install

```shell
pip install --upgrade falken-trace
```

### Usage
Add the `falken_trace` import at the beginning of the application entrypoint file

```python
import falken_trace  # noqa

from ddtrace import patch_all

...
```

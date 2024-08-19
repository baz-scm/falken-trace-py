# falken-trace-py

[![PyPI](https://img.shields.io/pypi/v/falken-trace)](https://pypi.org/project/falken-trace/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/falken-trace)](https://github.com/baz-scm/falken-trace-py)
![CodeQL](https://github.com/baz-scm/falken-trace-py/workflows/CodeQL/badge.svg)

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

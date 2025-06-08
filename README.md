<div align="center">
   <img align="center" width="128px" src="https://avatars.githubusercontent.com/u/140384842?s=200&v=4" />
   <h1 align="center"><b>falken-trace-py</b></h1>
   <p align="center">
      Enhance OpenTelemetry with pinpointed code-level observability for Python.
      <br />
      <a href="https://github.com/baz-scm/"><strong>Baz on GitHub »</strong></a>
      <br />
      <br />
      <b>Install via PyPI</b>
      <br />
      <code>pip install --upgrade falken-trace</code>
      <br />
      <br />
      <b>Libraries Available</b>
      <br />
      Python: <a href="https://github.com/baz-scm/falken-trace-py">falken-trace-py</a> · 
      Go: <a href="https://github.com/baz-scm/falken-trace-go">falken-trace-go</a>
   </p>
</div>

---

![PyPI](https://img.shields.io/pypi/v/falken-trace) 
![Python](https://img.shields.io/pypi/pyversions/falken-trace) 
![CodeQL](https://github.com/baz-scm/falken-trace-py/workflows/CodeQL/badge.svg)

## 🚀 What is Falken Trace?

Falken Trace extends OpenTelemetry and Datadog for Python by pinpointing **file names, function names**, and **line numbers** that generate spans. It addresses gaps in default observability implementations, making tracing faster and more actionable.

Default OpenTelemetry tracing for Python lacks this granularity, which we uncovered while building our contextual code review platform at [baz.co](https://baz.co).

With Falken Trace, troubleshooting becomes faster, more precise, and far more effective, giving you a crystal-clear view of codebase flows.

---
## Install

```shell
pip install falken-trace  # install via pip
poetry add falken-trace   # install via poetry
uv add falken-trace       # install via uv
```

## Usage
Add the `falken_trace` import at the beginning of the application entrypoint file

```python
import falken_trace  # noqa

from ddtrace import patch_all
```

# 🔗 Learn More
Go library: https://github.com/baz-scm/falken-trace-go

Blog post: [Extending OpenTelemetry to Pinpoint Code Elements](https://baz.co/resources/extending-opentelemetry-to-pinpoint-code-elements-our-journey-to-close-the-gap)

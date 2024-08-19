from __future__ import annotations


def test_wrap_dd_span_with_start_span() -> None:
    # given
    import falken_trace  # noqa

    from ddtrace import Tracer

    tracer = Tracer()

    # when
    span = tracer.start_span("test")

    # then
    tags = span.get_tags()

    assert tags.get("code.filepath") is None  # should be `None`, because the `tracer` decorator was not used
    assert tags.get("code.lineno") is None
    assert tags.get("code.func") is None
    assert tags.get("code.wrap_filepath").endswith("test_datadog.py")
    assert tags.get("code.wrap_lineno") == "13"
    assert tags.get("code.wrap_func") == "test_wrap_dd_span_with_start_span"


def test_wrap_dd_span_with_decorator() -> None:
    # given
    import falken_trace  # noqa

    from ddtrace import tracer, Span

    span: Span | None = None

    @tracer.wrap()
    def add(a: int, b: int) -> int:
        nonlocal span  # bind current span to check, if everything was set at the end
        span = tracer.current_span()
        return a + b

    # when
    add(22, 20)

    # then
    assert span is not None
    tags = span.get_tags()

    # making sure we have a relative path
    assert not tags.get("code.filepath").startswith("/")

    assert tags.get("code.filepath").endswith("test_datadog.py")
    assert tags.get("code.lineno") == "35"
    assert tags.get("code.func") == "add"
    assert tags.get("code.wrap_filepath").endswith("test_datadog.py")
    assert tags.get("code.wrap_lineno") == "41"
    assert tags.get("code.wrap_func") == "test_wrap_dd_span_with_decorator"


def test_disbale_falken_trace(disbale_falken_trace) -> None:
    # given
    import falken_trace  # noqa

    from ddtrace import Tracer

    tracer = Tracer()

    # when
    span = tracer.start_span("test")

    # then
    tags = span.get_tags()

    assert tags.get("code.wrap_filepath") is None
    assert tags.get("code.wrap_lineno") is None
    assert tags.get("code.wrap_func") is None

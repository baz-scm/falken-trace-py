def test_wrap_dd_span() -> None:
    # given
    import falken_trace  # noqa

    from ddtrace import Tracer

    tracer = Tracer()

    # when
    span = tracer.start_span("test")

    # then
    tags = span.get_tags()

    assert tags.get("code.filepath").endswith("test_falken.py")
    assert tags.get("code.lineno") == "10"
    assert tags.get("code.parent_func") == "test_wrap_dd_span"

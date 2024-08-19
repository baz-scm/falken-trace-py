from typing import Dict, Optional


def test_wrap_fastapi_entrypoint_span_with_sync_func() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: Optional[ddtrace.Span] = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.get("/")
    def hello() -> Dict[str, str]:
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return {"msg": "Hello World"}

    client = TestClient(app)

    # when
    client.get("/")

    # then
    tags = span.get_tags()

    assert tags.get("code.filepath").endswith("test_fastapi.py")
    assert tags.get("code.lineno") == "20"
    assert tags.get("code.func") == "hello"


def test_wrap_fastapi_entrypoint_span_with_async_func() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: Optional[ddtrace.Span] = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.get("/")
    async def ahello() -> Dict[str, str]:  # noqa: RUF029
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return {"msg": "Hello World"}

    client = TestClient(app)

    # when
    client.get("/")

    # then
    tags = span.get_tags()

    assert tags.get("code.filepath").endswith("test_fastapi.py")
    assert tags.get("code.lineno") == "54"
    assert tags.get("code.func") == "ahello"

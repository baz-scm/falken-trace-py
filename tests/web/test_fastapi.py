from typing import Annotated


def test_wrap_fastapi_entrypoint_span_with_sync_func() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: ddtrace.trace.Span | None = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.get("/")
    def hello() -> dict[str, str]:
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

    # make sure the cache was filled
    from falken_trace.common.cache import get_api_path_tags

    span_tags = get_api_path_tags("/")
    assert span_tags.file_path.endswith("test_fastapi.py")
    assert span_tags.line_number == "20"
    assert span_tags.func_name == "hello"


def test_wrap_fastapi_entrypoint_span_with_async_func() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: ddtrace.trace.Span | None = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.get("/hello-get")
    async def ahello() -> dict[str, str]:
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return {"msg": "Hello World"}

    client = TestClient(app)

    # when
    client.get("/hello-get")

    # then
    tags = span.get_tags()

    assert tags.get("code.filepath").endswith("test_fastapi.py")
    assert tags.get("code.lineno") == "62"
    assert tags.get("code.func") == "ahello"


def test_wrap_fastapi_entrypoint_span_with_str_payload() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import Body, FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: ddtrace.trace.Span | None = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.post("/hello-post")
    async def ahello(body: Annotated[str, Body(media_type="text/plain")]) -> dict[str, str]:
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return {"msg": f"Hello {body}"}

    client = TestClient(app)

    # when
    client.post("/hello-post", content="World", headers={"Content-Type": "text/plain"})

    # then
    tags = span.get_tags()

    assert tags.get("code.func") == "ahello"
    assert tags.get("params.body") == "World"


def test_wrap_fastapi_entrypoint_span_with_base_model_payload() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        description: str | None = None

    app = FastAPI()

    span: ddtrace.trace.Span | None = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.post("/items/")
    async def create_item(item: Item) -> Item:
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return item

    client = TestClient(app)

    payload = {"name": "Foo", "description": "An optional description"}

    # when
    client.post("/items/", json=payload)

    # then
    tags = span.get_tags()

    assert tags.get("code.func") == "create_item"
    assert tags.get("params.item.name") == "Foo"
    assert tags.get("params.item.description") == "An optional description"

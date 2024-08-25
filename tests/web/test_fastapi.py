from typing import Dict, Optional

from typing_extensions import Annotated


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
    assert tags.get("code.lineno") == "22"
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
    assert tags.get("code.lineno") == "56"
    assert tags.get("code.func") == "ahello"


def test_wrap_fastapi_entrypoint_span_with_str_payload() -> None:
    # given
    import falken_trace  # noqa

    import ddtrace

    ddtrace.patch(fastapi=True)

    from fastapi import Body, FastAPI
    from fastapi.testclient import TestClient

    app = FastAPI()

    span: Optional[ddtrace.Span] = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.post("/")
    async def ahello(body: Annotated[str, Body(media_type="text/plain")]) -> Dict[str, str]:  # noqa: RUF029
        nonlocal span  # bind current span to check, if everything was set at the end
        span = ddtrace.tracer.current_span()
        return {"msg": f"Hello {body}"}

    client = TestClient(app)

    # when
    client.post("/", content="World", headers={"Content-Type": "text/plain"})

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
        description: Optional[str] = None

    app = FastAPI()

    span: Optional[ddtrace.Span] = None  # can't use the newer syntax here, otherwise the FastAPI setup breaks

    @app.post("/items/")
    async def create_item(item: Item) -> Item:  # noqa: RUF029
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

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass

CACHE_API_ROUTES: OrderedDict[str, SpanTags] = OrderedDict()
CACHE_API_ROUTES_MAX_SIZE = 100


@dataclass
class SpanTags:
    file_path: str
    line_number: str
    func_name: str | None


def get_api_path_tags(path: str) -> SpanTags | None:
    return CACHE_API_ROUTES.get(path)


def set_api_path_tags(path: str, tags: SpanTags) -> None:
    CACHE_API_ROUTES[path] = tags
    if len(CACHE_API_ROUTES) > CACHE_API_ROUTES_MAX_SIZE:
        CACHE_API_ROUTES.popitem(last=False)

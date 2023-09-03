from __future__ import annotations

from typing import TYPE_CHECKING

import requests_cache

if TYPE_CHECKING:
    from arkruiter.types import JsonData

_session = requests_cache.CachedSession(
    "arkruiter",
    serializer="json",
    backend="filesystem",
    use_cache_dir=True,  # store in <platform-specific config dir>/arkruiter/
    cache_control=True,  # respect the cache-control header
    expire_after=0,  # if no header, expire immediately (still do conditional requests)
)


def download_json(url: str) -> JsonData:
    resp = _session.get(url, timeout=10)  # type: ignore reportUnknownMemberType
    resp.raise_for_status()
    return resp.json()

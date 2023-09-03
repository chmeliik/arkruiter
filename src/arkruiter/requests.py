from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests_cache

if TYPE_CHECKING:
    from arkruiter.types import JsonData

log = logging.getLogger(__name__)

_session = requests_cache.CachedSession(
    "arkruiter",
    serializer="json",
    backend="filesystem",
    use_cache_dir=True,  # store in <platform-specific config dir>/arkruiter/
    cache_control=True,  # respect the cache-control header
    expire_after=0,  # if no header, expire immediately (still do conditional requests)
)


def download_json(url: str) -> JsonData:
    log.debug("Getting data from %s", url)
    resp = _session.get(url, timeout=10)  # type: ignore reportUnknownMemberType
    log.debug("Response was cached: %r", resp.from_cache)
    resp.raise_for_status()
    return resp.json()

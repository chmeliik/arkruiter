from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from arkruiter.types import JsonData

log = logging.getLogger(__name__)

_session = requests.session()


def download_json(url: str) -> JsonData:
    log.info("Downloading data from %s", url)
    resp = _session.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

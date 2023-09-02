from __future__ import annotations

from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from arkruiter.types import JsonData

_session = requests.session()


def download_json(url: str) -> JsonData:
    resp = _session.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

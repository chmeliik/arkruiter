from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import NoneType

JsonData = (
    NoneType
    | bool
    | int
    | float
    | str
    | Sequence["JsonData"]
    | Mapping[str, "JsonData"]
)

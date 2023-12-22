from __future__ import annotations

import re
from collections.abc import Sequence  # noqa: TCH003
from typing import Self

import pydantic

from arkruiter.requests import download_json

DEFAULT_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData_YoStar/master/en_US/gamedata/excel/gacha_table.json"


class Tag(pydantic.BaseModel):
    tag_name: str = pydantic.Field(alias="tagName")


class GachaTable(pydantic.BaseModel):
    gacha_tags: Sequence[Tag] = pydantic.Field(alias="gachaTags")
    recruit_detail: str = pydantic.Field(alias="recruitDetail")

    def is_recruitable(self, character_name: str) -> bool:
        # Matches:
        # <@rc.eml>'Justice Knight'</> <- 'Justice Knight'
        # <@rc.eml>Yato</>             <- Yato
        # / Fang /                     <- Fang
        # / Spot$                      <- Spot
        # ^Exusiai /                   <- Exusiai
        pattern = rf"(^|/ |>){re.escape(character_name)}(<| /|$)"
        return re.search(pattern, self.recruit_detail, re.MULTILINE) is not None

    @classmethod
    def from_url(cls, url: str = DEFAULT_URL) -> Self:
        return cls.model_validate(download_json(url))

from __future__ import annotations

import enum
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, NamedTuple, Self

import pydantic

from arkruiter.requests import download_json

if TYPE_CHECKING:
    from arkruiter.types import JsonData

DEFAULT_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/en_US/gamedata/excel/character_table.json"


class Rarity(int, enum.Enum):
    Six = 5
    Five = 4
    Four = 3
    Three = 2
    Two = 1
    One = 0


class Position(str, enum.Enum):
    Melee = "MELEE"
    Ranged = "RANGED"


class Profession(str, enum.Enum):
    Caster = "CASTER"
    Medic = "MEDIC"
    Vanguard = "PIONEER"
    Sniper = "SNIPER"
    Specialist = "SPECIAL"
    Supporter = "SUPPORT"
    Defender = "TANK"
    Guard = "WARRIOR"


class Character(pydantic.BaseModel):
    name: str
    rarity: Rarity
    tags: Sequence[str] = pydantic.Field(alias="tagList")
    position: Position
    profession: Profession


class CharacterTable(NamedTuple):
    characters: Sequence[Character]

    @classmethod
    def from_json(cls, json_data: JsonData) -> Self:
        validated_data = pydantic.TypeAdapter(
            Mapping[str, Mapping[str, Any]]
        ).validate_python(json_data)

        characters = [
            Character.model_validate(character_data)
            for character_data in validated_data.values()
            if character_data.get("itemObtainApproach") is not None
        ]
        return cls(characters)

    @classmethod
    def from_url(cls, url: str = DEFAULT_URL) -> Self:
        return cls.from_json(download_json(url))

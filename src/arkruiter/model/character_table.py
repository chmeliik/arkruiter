from __future__ import annotations

import enum
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal, NamedTuple, Self

import pydantic

if TYPE_CHECKING:
    from arkruiter.types import JsonData

Position = Literal["MELEE", "RANGED"]


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
    rarity: int
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

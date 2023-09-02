from __future__ import annotations

from typing import TYPE_CHECKING

from arkruiter.model.character_table import Character, CharacterTable, Profession

if TYPE_CHECKING:
    from arkruiter.types import JsonData

AMIYA = Character(
    name="Amiya",
    rarity=4,
    tagList=["DPS"],
    position="RANGED",
    profession=Profession.Caster,
)


def test_parse_character() -> None:
    character = Character.model_validate(
        {
            "name": "Amiya",
            "rarity": 4,
            "tagList": ["DPS"],
            "position": "RANGED",
            "profession": "CASTER",
        }
    )
    assert character == AMIYA


def test_character_table_from_json() -> None:
    table_data: JsonData = {
        "char_002_amiya": {
            "name": "Amiya",
            # ...
            "position": "RANGED",
            "tagList": ["DPS"],
            # ...
            "itemObtainApproach": "Main Story",
            # ...
            "rarity": 4,
            "profession": "CASTER",
            # ...
        },
        "char_509_acast": {
            "name": "Pith",
            # ...
            "position": "RANGED",
            "tagList": ["AoE"],
            "itemObtainApproach": None,
            # ...
            "rarity": 4,
            "profession": "CASTER",
            # ...
        },
    }
    table = CharacterTable.from_json(table_data)
    assert table.characters == [AMIYA]

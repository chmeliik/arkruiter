from __future__ import annotations

import functools
from dataclasses import dataclass

from arkruiter.game_data import character_table, gacha_table

__all__ = [
    "Character",
    "GameData",
    "Rarity",
]

Character = character_table.Character
Rarity = character_table.Rarity


@dataclass(frozen=True)
class GameData:
    character_table_url: str = character_table.DEFAULT_URL
    gacha_table_url: str = gacha_table.DEFAULT_URL

    def recruitment_tags(self) -> list[str]:
        return [
            tag_name
            for tag in self._gacha_table.gacha_tags
            if (tag_name := tag.tag_name) not in ("Male", "Female")
        ]

    def recruitable_characters(self) -> list[Character]:
        return [
            c
            for c in self._character_table.characters
            if self._gacha_table.is_recruitable(c.name)
        ]

    @functools.cached_property
    def _gacha_table(self) -> gacha_table.GachaTable:
        return gacha_table.GachaTable.from_url(self.gacha_table_url)

    @functools.cached_property
    def _character_table(self) -> character_table.CharacterTable:
        return character_table.CharacterTable.from_url(self.character_table_url)

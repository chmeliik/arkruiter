from __future__ import annotations

import enum
import functools
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self

from arkruiter.game_data import Character, Rarity

if TYPE_CHECKING:
    from collections.abc import Sequence


class Interest(int, enum.Enum):
    SixStar = 4
    FiveStar = 3
    Robot = 2
    FourStar = 1
    NoInterest = 0


@dataclass(frozen=True)
class RecruitmentResult:
    possible_characters: Sequence[Character]
    selected_tags: Sequence[str]

    def __lt__(self, other: Self) -> bool:
        def key(r: RecruitmentResult) -> tuple[Interest, int]:
            return r.interest, -len(r.possible_characters)

        return key(self) < key(other)

    @functools.cached_property
    def interest(self) -> Interest:
        if not self.possible_characters:
            return Interest.NoInterest

        def rarity(c: Character) -> int:
            return c.rarity

        lowest_guaranteeable_rarity = min(
            filter(lambda r: r > Rarity.Two, map(rarity, self.possible_characters)),
            default=Rarity.Three,
        )

        if lowest_guaranteeable_rarity == Rarity.Six:
            interest = Interest.SixStar
        elif lowest_guaranteeable_rarity == Rarity.Five:
            interest = Interest.FiveStar
        elif lowest_guaranteeable_rarity == Rarity.Four:
            interest = Interest.FourStar
        else:
            interest = Interest.NoInterest

        if max(self.possible_characters, key=rarity).rarity == Rarity.One:
            interest = max(interest, Interest.Robot)

        return interest

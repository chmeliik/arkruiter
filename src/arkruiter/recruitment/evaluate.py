from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from arkruiter.game_data import Character, Rarity
from arkruiter.recruitment.result import RecruitmentResult

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

SIX_STAR_TAG = "Top Operator"
FIVE_STAR_TAG = "Senior Operator"
ONE_STAR_TAG = "Robot"


def try_all_combinations(
    available_tags: Sequence[str], recruitable_characters: Sequence[Character]
) -> Iterable[RecruitmentResult]:
    tag_selections = (
        selection
        for n in range(1, 4)
        for selection in itertools.combinations(available_tags, n)
    )
    return (
        RecruitmentResult(
            possible_characters=_filter_by_tags(recruitable_characters, selected_tags),
            selected_tags=selected_tags,
        )
        for selected_tags in tag_selections
    )


def _filter_by_tags(
    characters: Iterable[Character], tags: Sequence[str]
) -> list[Character]:
    return [c for c in characters if _is_recruitable_by_tags(c, tags)]


def _is_recruitable_by_tags(character: Character, tags: Sequence[str]) -> bool:
    if character.rarity == Rarity.Six and SIX_STAR_TAG not in tags:
        return False
    return all(_has_tag(character, tag) for tag in tags)


def _has_tag(character: Character, tag_name: str) -> bool:
    relevant_tags = (
        *character.tags,
        character.profession.name,
        character.position.name,
        _rarity_tag(character),
    )
    return tag_name in relevant_tags


def _rarity_tag(character: Character) -> str | None:
    if character.rarity == Rarity.Six:
        return SIX_STAR_TAG
    elif character.rarity == Rarity.Five:
        return FIVE_STAR_TAG
    elif character.rarity == Rarity.One:
        return ONE_STAR_TAG
    else:
        return None

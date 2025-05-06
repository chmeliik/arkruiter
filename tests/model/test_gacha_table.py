from __future__ import annotations

import textwrap

import pytest

from arkruiter.game_data.gacha_table import GachaTable


@pytest.mark.network
def test_gacha_table_from_url() -> None:
    table = GachaTable.from_url()
    tag_names = [tag.tag_name for tag in table.gacha_tags]
    assert tag_names == [
        "Guard",
        "Sniper",
        "Defender",
        "Medic",
        "Supporter",
        "Caster",
        "Specialist",
        "Vanguard",
        "Melee",
        "Ranged",
        "Top Operator",
        "Crowd-Control",
        "Nuker",
        "Senior Operator",
        "Healing",
        "Support",
        "Starter",
        "DP-Recovery",
        "DPS",
        "Survival",
        "AoE",
        "Defense",
        "Slow",
        "Debuff",
        "Fast-Redeploy",
        "Shift",
        "Summon",
        "Robot",
        "Elemental",
        "Male",
        "Female",
    ]


def test_is_recruitable() -> None:
    # <@rc.eml>'Justice Knight'</> <- 'Justice Knight'
    # <@rc.eml>Yato</>             <- Yato
    # / Fang /                     <- Fang
    # / Spot$                      <- Spot
    # ^Exusiai /                   <- Exusiai
    table = GachaTable(
        gachaTags=[],
        recruitDetail=textwrap.dedent(
            """
            <@rc.eml>'Justice Knight'</>
            <@rc.eml>Yato</>
            / Fang /
            / Spot
            Exusiai / Silver Ash
            """
        ),
    )
    assert table.is_recruitable("'Justice Knight'")
    assert table.is_recruitable("Yato")
    assert table.is_recruitable("Fang")
    assert table.is_recruitable("Spot")
    assert table.is_recruitable("Exusiai")
    assert table.is_recruitable("Silver Ash")
    assert not table.is_recruitable("Ash")

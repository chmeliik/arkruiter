from __future__ import annotations

import argparse
import shlex
import textwrap
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal

from arkruiter.game_data import GameData
from arkruiter.recruitment import try_all_combinations

if TYPE_CHECKING:
    from collections.abc import Sequence


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", nargs="+", help="select a recruitment tag")
    ap.add_argument(
        "--print-completion",
        choices=["zsh"],
        action=PrintCompletionAction,
        help="print completion for the selected shell and exit",
    )
    args = ap.parse_args()

    game_data = GameData()
    tags: list[str] = args.tag

    interesting_results = sorted(
        filter(
            lambda r: r.interest != 0,
            try_all_combinations(tags, game_data.recruitable_characters()),
        )
    )

    if interesting_results:
        for result in interesting_results:
            print("-" * 80)
            _print_wrapped(f"tags: {', '.join(result.selected_tags)}")
            _print_wrapped(
                f"characters: {', '.join(c.name for c in result.possible_characters)}"
            )
    else:
        print("-" * 80)
        print("Nothing interesting")
    print("-" * 80)


def _print_wrapped(text: str, width: int = 80) -> None:
    print("\n".join(textwrap.wrap(text, width, subsequent_indent=" " * 4)))


class PrintCompletionAction(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        _namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        _option_string: str | None = None,
    ) -> None:
        if values == "zsh":
            code = self._completion_code("zsh")
        else:
            parser.error(f"unknown shell: {values}")

        print(code.strip())
        parser.exit(0)

    def _completion_code(self, shell: Literal["zsh"]) -> str:
        recruitment_tags = self._get_recruitment_tags()
        if shell == "zsh":
            quoted_tags = " ".join(map(shlex.quote, recruitment_tags))
            code = dedent(
                f"""
                _arkruiter() {{
                    local -a tags
                    tags=({quoted_tags})
                    _describe 'arkruiter' tags
                }}

                compdef _arkruiter arkruiter
                """
            )
        return code

    def _get_recruitment_tags(self) -> list[str]:
        return GameData().recruitment_tags()

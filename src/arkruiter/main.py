from __future__ import annotations

import argparse
import logging
import shlex
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal

from arkruiter.game_data.gacha_table import GachaTable

if TYPE_CHECKING:
    from collections.abc import Sequence


log = logging.getLogger(__name__)


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

    tags: list[str] = args.tag
    print("\n".join(tags))


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
        gacha_table = GachaTable.from_url()
        return [
            tag_name
            for tag in gacha_table.gacha_tags
            if (tag_name := tag.tag_name) not in ("Male", "Female")
        ]

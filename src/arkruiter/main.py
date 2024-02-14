from __future__ import annotations

import argparse
import logging
import shlex
import shutil
import textwrap
from textwrap import dedent
from typing import TYPE_CHECKING, Any, Literal, assert_never

from arkruiter.game_data import GameData
from arkruiter.logging import setup_root_logger
from arkruiter.recruitment import try_all_combinations

if TYPE_CHECKING:
    from collections.abc import Sequence

log = logging.getLogger(__name__)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", nargs="+", help="select a recruitment tag")
    ap.add_argument(
        "--print-completion",
        choices=["bash", "zsh"],
        action=PrintCompletionAction,
        help="print completion for the selected shell and exit",
    )
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    setup_root_logger("arkruiter", logging.DEBUG if args.verbose else logging.INFO)

    game_data = GameData()
    tags = _validify_tags(args.tag, game_data.recruitment_tags())

    interesting_results = sorted(
        filter(
            lambda r: r.interest != 0,
            try_all_combinations(tags, game_data.recruitable_characters()),
        ),
        reverse=True,
    )

    terminal_width, _ = shutil.get_terminal_size()

    if interesting_results:
        for result in interesting_results:
            print("-" * terminal_width)
            _print_wrapped(f"tags: {', '.join(result.selected_tags)}")
            _print_wrapped(
                f"characters: {', '.join(c.name for c in result.possible_characters)}",
                width=terminal_width,
            )
    else:
        print("-" * terminal_width)
        print("Nothing interesting")
    print("-" * terminal_width)


def _validify_tags(
    user_tags: Sequence[str], recruitment_tags: Sequence[str]
) -> list[str]:
    """Convert lowercase tags to their correct-case variants, drop unknown tags."""
    valid_tags: list[str] = []
    lower_tag_to_actual_tag = {tag.lower(): tag for tag in recruitment_tags}
    for tag in user_tags:
        actual_tag = lower_tag_to_actual_tag.get(tag.lower())
        if actual_tag:
            valid_tags.append(actual_tag)
        else:
            log.warning("Unknown tag: %r", tag)
    return valid_tags


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
        shell = values
        if shell in ("bash", "zsh"):
            code = self._completion_code(shell)
        else:
            parser.error(f"unknown shell: {shell}")

        print(code.strip())
        parser.exit(0)

    def _completion_code(self, shell: Literal["bash", "zsh"]) -> str:
        recruitment_tags = self._get_recruitment_tags()
        quoted_tags = " ".join(map(shlex.quote, recruitment_tags))
        if shell == "zsh":
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
        elif shell == "bash":
            double_quoted_tags = shlex.quote(quoted_tags)
            code = f"complete -W {double_quoted_tags} arkruiter"
        else:
            assert_never(shell)
        return code

    def _get_recruitment_tags(self) -> list[str]:
        return GameData().recruitment_tags()

from __future__ import annotations

import argparse


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("tag", nargs="+", help="select a recruitment tag")
    args = ap.parse_args()

    tags: list[str] = args.tag
    print("\n".join(tags))

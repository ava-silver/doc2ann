#! /usr/bin/env python3

# stdlib
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path

# project
from runner import run


def main() -> None:
    parser = ArgumentParser(
        description="Tool to translate docstring types to annotations."
    )
    parser.add_argument("src", nargs="+", type=Path)
    parser.add_argument(
        "-d", "--dry-run", "--diff", dest="dry_run", action="store_true", default=False
    )
    parser.add_argument(
        "-D", "--debug", dest="debug", action="store_true", default=False
    )
    parser.add_argument(
        "--convert-caret-to-bracket", action="store_true", default=False
    )
    parser.add_argument(
        "--unparseable-types",
        type=str,
        choices=["allow", "drop", "str"],
        default="allow",
    )
    options = dict(parser.parse_args().__dict__)
    run(options.pop("src"), **options)
    print("All done!")


if __name__ == "__main__":
    main()

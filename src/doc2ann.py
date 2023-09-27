#! /usr/bin/env python3

# stdlib
from __future__ import annotations
from argparse import ArgumentParser
from pathlib import Path
from sys import stderr

# project
from runner import run


def main() -> None:
    parser = ArgumentParser(
        description="Tool to translate docstring types to annotations."
    )
    parser.add_argument("src", nargs="+", type=Path)
    parser.add_argument(
        "-d",
        "--dry-run",
        "--diff",
        dest="dry_run",
        action="store_true",
        default=False,
        help="Print a diff instead of modifying the file.",
    )
    parser.add_argument(
        "-D",
        "--debug",
        dest="debug_mode",
        action="store_true",
        default=False,
        help="Enable debug mode, useful for debugging weird errors",
    )
    parser.add_argument(
        "--preserve-angle-brackets",
        action="store_true",
        default=False,
        help="Preserve `<` and `>` instead of replacing them with `[` and `]`",
    )
    parser.add_argument(
        "--unparseable-types",
        type=str,
        choices=["allow", "drop", "str"],
        default="str",
        help="""Behavior when encountering invalid python types:
        - (allow) keep them as is
        - (str) make them in string form so the program will still run
        - (drop) remove them entirely from the signature""",
    )
    parser.add_argument(
        "--keep-arg-description",
        action="store_true",
        default=False,
        help="Keep the description for arguments, only remove the types. "
        "Default behavior is to remove Args/Return sections.",
    )
    options = dict(parser.parse_args().__dict__)
    run(options.pop("src"), **options)
    print("All done!", file=stderr)


if __name__ == "__main__":
    main()

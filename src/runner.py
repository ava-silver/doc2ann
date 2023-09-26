# stdlib
from __future__ import annotations
from itertools import chain as flatten
from pathlib import Path
from sys import stderr

# 3p
from refactor import Session
from refactor.runner import expand_paths

# project
from fix_docstring import Doc2AnnConfig, FixDocstring, SEEN_FUNCTIONS


def run(
    file_paths: list[Path],
    dry_run: bool,
    **options,
) -> None:
    session = Session(
        rules=[FixDocstring],
        config=Doc2AnnConfig(**options),
    )
    files = flatten.from_iterable(
        expand_paths(source_dest) for source_dest in file_paths
    )
    if not files:
        raise SystemExit(1)
    for file in files:
        SEEN_FUNCTIONS.clear()
        change = session.run_file(file)
        if not change:
            continue
        elif dry_run:
            print(change.compute_diff())
        else:
            print(f"reformatted {change.file!s}", file=stderr)
            change.apply_diff()

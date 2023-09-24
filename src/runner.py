# stdlib
from __future__ import annotations
from dataclasses import dataclass
from itertools import chain as flatten
from pathlib import Path
from sys import stderr

# 3p
from refactor import Session, Configuration
from refactor.runner import expand_paths

# project
from fix_docstring import FixDocstring, UnparseableBehavior


@dataclass
class Doc2AnnConfig(Configuration):
    convert_caret_to_bracket: bool = False
    unparseable_types: UnparseableBehavior = "str"


def run(
    file_paths: list[Path],
    dry_run: bool,
    debug: bool = False,
    **options,
) -> None:
    session = Session(
        rules=[FixDocstring], config=Doc2AnnConfig(debug_mode=debug, **options)
    )
    files = flatten.from_iterable(
        expand_paths(source_dest) for source_dest in file_paths
    )
    if not files:
        raise SystemExit(1)
    for file in files:
        change = session.run_file(file)
        if not change:
            continue
        elif dry_run:
            print(change.compute_diff())
        else:
            print(f"reformatted {change.file!s}", file=stderr)
            change.apply_diff()

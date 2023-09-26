from os import listdir
from pathlib import Path
from pytest import CaptureFixture, mark

from doc2ann import run

FIXTURES_DIR = Path("src", "test", "fixtures")


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def get_tests() -> list[tuple[list[Path], str]]:
    return [
        ([file := FIXTURES_DIR.joinpath(f)], read_file(f"{file}.diff"))
        for f in listdir(FIXTURES_DIR)
        if f.endswith(".py")
    ]


@mark.parametrize("input_files, output_diff", get_tests())
def test_example(
    capsys: CaptureFixture[str],
    input_files: list[Path],
    output_diff: str,
):
    run(
        input_files,
        dry_run=True,
        convert_caret_to_bracket=True,
        unparseable_types="allow",
        drop_arg_description=True,
    )
    captured = capsys.readouterr()
    breakpoint()
    assert captured.out == output_diff

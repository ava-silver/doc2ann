from pathlib import Path
from pytest import mark

from doc2ann import run


def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


def get_tests() -> list[tuple[list[Path], str]]:
    single_file_tests = ["src/test/fixtures/hi.py"]
    return [([Path(f)], read_file(f + ".diff")) for f in single_file_tests]


@mark.parametrize("input_files, output_diffs", get_tests())
def test_example(capsys, input_files, output_diffs):
    run(input_files, dry_run=True, convert_caret_to_bracket=True)
    captured = capsys.readouterr()
    assert captured.out == output_diffs

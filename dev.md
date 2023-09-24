# Development

## Setup

```bash
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -e ".[dev]"
```

## Build

To build, confirm the version number in `pyproject.toml` is up to date, and then run:
```bash
$ python3 -m build
```

## Distribute
```bash
$ python3 -m twine upload -r pypi dist/doc2ann-<version>*
```


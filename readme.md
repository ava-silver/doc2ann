# doc2ann

Inspired by [com2ann](https://github.com/ilevkivskyi/com2ann), I wanted to create a similar tool for converting docstring comments.


## Usage:

Install the dependencies:
```bash
$ pip install -e .
```
Running

```bash
$ doc2ann -a your_file.py
```


## Development

### Setup

```bash
$ virtualenv .venv
$ . .venv/bin/activate
$ pip install -e ".[dev]"
```

### Build

To build, confirm the version number in `pyproject.toml` is up to date, and then run:
```bash
$ ./build.sh
```
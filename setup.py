#!/usr/bin/env python

import sys
from setuptools import setup

if sys.version_info < (3, 8, 0):
    sys.stderr.write("ERROR: You need Python 3.8 or later to use doc2ann.\n")
    exit(1)

version = "0.0.1"
description = "Tool to translate docstring types to annotations."
long_description = """
doc2ann
=======

Tool for translation of typed docstrings to type annotations in Python.

This tool requires Python 3.8 to run. But the supported target code version
is Python 3.4+ (can be specified with ``--python-minor-version``).

Currently, the tool translates function and method docstrings to type annotations.""".lstrip()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.8",
    "Topic :: Software Development",
]

setup(
    name="doc2ann",
    version=version,
    description=description,
    long_description=long_description,
    author="Ava Silver",
    author_email="ava@avasilver.dev",
    url="https://github.com/ava-silver/doc2ann",
    license="MIT",
    keywords="docstring doc pydoc typing function annotations type hints variable annotations",
    python_requires=">=3.8",
    package_dir={"": "src"},
    py_modules=["doc2ann"],
    entry_points={"console_scripts": ["doc2ann=doc2ann:main"]},
    classifiers=classifiers,
)

#!/bin/bash
set -exuo pipefail
version=`grep -oP 'version\s*=\s*"\K[^"]+' pyproject.toml`
mkdir -p dist/$version
pip wheel . --require-virtualenv -w dist/$version

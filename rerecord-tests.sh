#!/bin/bash
find src/test/fixtures -name '*.py' -exec bash -c "doc2ann -d {} > {}.diff" \;
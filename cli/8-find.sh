#!/bin/sh
# Where a value went: every document, pipeline step and host it reached. Reports hold
# a fingerprint of each identifier, never the value, so the search reads no values.
# Run `make trace` first and the answer also names the pipeline steps and the vector
# store that hold it.
set -e

uv run complydoc audit documents --no-ocr --name audit -q
uv run complydoc find "DE89 3704 0044 0532 0130 00"

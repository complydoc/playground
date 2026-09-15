#!/bin/sh
# Audit a folder: token cost, extraction readiness, identifiers and hidden content.
# Writes out/audit.html and out/audit.json.
set -e

uv run complydoc audit documents --no-ocr --out out --name audit

# One component at a time, printed as JSON for another tool.
uv run complydoc sensitive documents/employee-record.pdf --no-ocr --print-json \
  | uv run python -c "import json, sys; r = json.load(sys.stdin); print(r['aggregate']['sensitive_total'], 'identifiers')"

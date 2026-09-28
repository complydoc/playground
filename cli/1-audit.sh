#!/bin/sh
# Audit a folder: token cost, extraction readiness, identifiers and hidden content.
# Writes .complydoc/audit.json; `uv run complydoc ui` opens it.
set -e

uv run complydoc audit documents --no-ocr --name audit

# One component at a time, printed as JSON for another tool.
uv run complydoc sensitive documents/company/employee-handbook.pdf --no-ocr --print-json \
  | uv run python -c "import json, sys; r = json.load(sys.stdin); print(r['aggregate']['sensitive_total'], 'identifiers')"

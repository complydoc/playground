#!/bin/sh
# The policy packs complydoc ships, run on one audit: finance, legal and hr.
# Each fails on these documents on purpose; see policy.yaml for why.
set -e

uv run complydoc audit documents --no-ocr --name audit -q
for pack in finance legal hr; do
  echo "== $pack"
  uv run complydoc check --report .complydoc/audit.json --policy "$pack" \
    || echo "complydoc check --policy $pack exits with status $?"
done

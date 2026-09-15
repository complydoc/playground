#!/bin/sh
# Compare a new audit with the committed baseline, as the CI workflow does.
# Exits 1 when something got worse. Writes out/diff.html and out/diff.json.
set -e

uv run complydoc audit documents --no-ocr --no-page-images --no-extracted-text \
  --out out --name current -q
uv run complydoc diff baseline/report.json out/current.json --out out --name diff

# A regression on purpose: the baseline against a report of one document, so the
# other documents count as removed. --no-fail-on-regression keeps the exit code 0.
uv run complydoc sensitive documents/employee-record.pdf --no-ocr --out out --name one -q
uv run complydoc diff baseline/report.json out/one.json --no-fail-on-regression -q
if uv run complydoc diff baseline/report.json out/one.json -q; then
  echo "no regression"
else
  echo "without the flag, complydoc diff exits with status $?"
fi

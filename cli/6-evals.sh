#!/bin/sh
# Check documents/.complydoc-evals.yaml against what each reader returns: passages and
# totals that must survive, and the hidden instruction, which must not.
# Writes .complydoc/evals.json; in `uv run complydoc ui`, open the Evals page.
set -e

uv run complydoc audit documents --no-ocr --compare-extractor pypdf --name evals -q
uv run python - <<'PY'
import json

evals = json.load(open(".complydoc/evals.json"))["evals"]
for check in evals["checks"]:
    held = ", ".join(f"{reader} {'yes' if found else 'no'}" for reader, found in check["found"].items())
    print(f"{check['kind']:6}  {check['fact'][:60]:60}  {held}")
PY

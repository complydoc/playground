#!/bin/sh
# Run two LangChain PDF loaders on the same files and report where they differ:
# text, identifiers, metadata, network attempts and the expected fact.
# Writes out/loaders.html and out/loaders.json.
set -e

uv run complydoc compare-loaders cli/loaders.yaml --out out --name loaders

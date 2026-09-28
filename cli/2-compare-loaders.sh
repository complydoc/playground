#!/bin/sh
# Run two LangChain PDF loaders on the same files and report where they differ:
# text, identifiers, metadata, network attempts and the expected fact.
# Writes .complydoc/loaders.json; in `uv run complydoc ui`, open a document's Diff.
set -e

uv run complydoc compare-loaders cli/loaders.yaml --name loaders

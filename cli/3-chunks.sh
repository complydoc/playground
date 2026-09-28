#!/bin/sh
# Compare two chunk sizes: token statistics, cut sentences and tables, identifiers
# repeated across chunks, and whether the expected fact stays in one chunk.
# Writes .complydoc/chunks.json, with masked previews only.
set -e

uv run complydoc chunks documents --no-ocr \
  --splitter "langchain_text_splitters:RecursiveCharacterTextSplitter chunk_size=300 chunk_overlap=0" \
  --splitter "langchain_text_splitters:RecursiveCharacterTextSplitter chunk_size=1200 chunk_overlap=100" \
  --fact "Evidence may be requested for any answer during the on-site review." \
  --max-tokens 400 --name chunks

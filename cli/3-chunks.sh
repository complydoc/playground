#!/bin/sh
# Compare two chunk sizes: token statistics, cut sentences and tables, identifiers
# repeated across chunks, and whether the expected fact stays in one chunk.
# Writes out/chunks.html and out/chunks.json, with masked previews only.
set -e

uv run complydoc chunks documents --no-ocr \
  --splitter "langchain_text_splitters:RecursiveCharacterTextSplitter chunk_size=300 chunk_overlap=0" \
  --splitter "langchain_text_splitters:RecursiveCharacterTextSplitter chunk_size=1200 chunk_overlap=100" \
  --fact "Two administrator accounts have no multi-factor authentication" \
  --max-tokens 400 --out out --name chunks

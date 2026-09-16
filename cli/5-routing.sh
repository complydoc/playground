#!/bin/sh
# Which extraction path each page needs — its text layer, local OCR, or a vision
# model — with the reason, and what that mix costs against sending everything one
# way. Writes out/routing.json, a manifest an ingestion job can read.
set -e

uv run complydoc routing documents --no-ocr --out out --name routing

# complydoc playground

Runnable examples of [complydoc](https://github.com/complydoc/complydoc), from the command
line and from Python, over the sample documents in `documents/`. The samples are synthetic
and contain made-up identifiers and one hidden instruction on purpose.

Documentation: <https://complydoc.github.io/complydoc/>

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
make setup
```

This installs complydoc with pandas, LangChain's PDF loaders (`pypdf`, `pdfplumber`),
LangChain text splitters and pytest. OCR and name detection are left out, so the examples
run with `--no-ocr` and report that names were not scanned.

## Command line

| Script | What it runs |
| --- | --- |
| `cli/1-audit.sh` | `complydoc audit` on the folder, and `complydoc sensitive --print-json` on one file |
| `cli/2-compare-loaders.sh` | `complydoc compare-loaders cli/loaders.yaml`: PyPDF and pdfplumber on the same files, with an expected fact |
| `cli/3-chunks.sh` | `complydoc chunks` with two chunk sizes of `RecursiveCharacterTextSplitter` |
| `cli/4-diff.sh` | `complydoc diff` against `baseline/report.json`, and its exit code on a regression |
| `cli/5-routing.sh` | `complydoc routing`: the path each page needs, priced as a mix, written as a manifest |

`make cli` runs all five. Reports are written to `out/`.

## Python

| Script | API |
| --- | --- |
| `python/01_audit_a_folder.py` | `full_audit`, `write_html`, `write_json` |
| `python/02_strings.py` | `scan_text`, `mask_text`, `find_hidden`, `count_tokens` |
| `python/03_inspect_a_loader.py` | `inspect_documents` on a LangChain loader |
| `python/04_compare_loaders.py` | `compare_loaders` over files, with facts and a loader cache |
| `python/05_chunks.py` | `extract_text`, `compare_chunkers`, `write_chunks_html` |
| `python/06_pipeline_steps.py` | `StripPathMetadata`, `DropHiddenPassages`, `MaskIdentifiers` on LangChain documents |
| `python/07_baseline_and_diff.py` | `load_report`, `diff_reports`, `write_diff_html` |
| `python/08_extend.py` | `register_detector`, `register_signal`, `Config.override` |
| `python/09_report_tables.py` | `report.to_pandas`, `iter_audit` |

`make python` runs all nine from the repository root.

## Tests and CI

`tests/test_documents.py` uses `cd.expect` to check the documents: nothing regressed
against the baseline, the terms hold no high-severity identifiers, the hidden instruction in
the vendor assessment is caught, and the loader made no network connection. `make test`
runs it.

`.github/workflows/documents.yml` audits the folder on every push, runs `complydoc diff`
against the baseline (failing on a regression), runs the tests and uploads the reports.

After changing the documents on purpose, `make baseline` rewrites `baseline/report.json`.

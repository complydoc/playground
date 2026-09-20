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

Reports mask every identifier they find, in the page text as well as the findings, and draw
each page as a wireframe rather than a picture. `--reveal` and `--page-images` change that,
and both say so when they do.

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

## Policy

`policy.yaml` is the same checks written as rules, for `complydoc check`:

```bash
uv run complydoc check documents --policy policy.yaml --no-ocr
```

It fails on purpose. These samples are built to be found: the vendor assessment hides an
instruction to a model in white text, and the employee record is a full set of identifiers.
A folder that passed would show nothing worth reading. Names are reported as not scanned
rather than failing, because this playground installs no name model.

## Tests and CI

`tests/test_documents.py` uses `cd.expect` to check the documents: nothing regressed
against the baseline, the terms hold no high-severity identifiers, the hidden instruction in
the vendor assessment is caught, and the loader made no network connection. `make test`
runs it.

`.github/workflows/documents.yml` gates the repository two ways, one job each:

- **policy**: the [complydoc action](https://complydoc.github.io/complydoc/guides/github-action/)
  runs `check` against `policy.yaml`, writes the result to the job summary and keeps one
  comment on the pull request up to date. It is set to `fail: false`, so the deliberate
  failures above do not turn the run red; drop that where a failure should stop a merge.
- **baseline**: audits the folder, runs `complydoc diff` against the committed baseline
  (failing on a regression), runs the tests and uploads the reports.

After changing the documents on purpose, `make baseline` rewrites `baseline/report.json`.

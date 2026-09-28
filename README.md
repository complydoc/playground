# complydoc playground

Runnable examples of [complydoc](https://github.com/complydoc/complydoc), the observability
layer for AI ingestion pipelines, on LangChain loaders and splitters. The documents are
synthetic, in two folders:

- `documents/company/`: an annual report, a two-column services agreement, a handbook,
  a due diligence questionnaire and a CV.
- `documents/invoices/`: German invoices, scanned invoices and a refund request by email.

Every identifier in them is made up, and two hide an instruction to a model on purpose.

Documentation: <https://complydoc.github.io/complydoc/docs/>

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
make setup
```

This installs complydoc with pandas, LangChain's PDF loaders (`PyPDFLoader`,
`PyMuPDF4LLMLoader`, `PDFPlumberLoader`), LangChain text splitters and pytest. OCR and name
detection are left out, so the examples run with `--no-ocr` and report that names were not
scanned.

## Start here

```bash
make start
make ui
```

`pipeline.py` is a LangChain ingestion pipeline inside `cd.observe`: the company
documents loaded with `PyMuPDF4LLMLoader`, the invoices with `PyPDFLoader`, then cleaned,
split and embedded. `make start` runs it twice, as written and with `--mask`, and compares two
LangChain PDF loaders on the same files. `make ui` opens the runs in your browser:

- **Trace**: each LangChain call as a step, with its time, tokens, cost, and the
  identifiers it passed on. Runs, with both ticked, shows what masking changed.
- **Documents**: which loader to use for PDFs, and a document's Diff, `PyPDFLoader`
  against `PyMuPDF4LLMLoader`, line by line.

The embedding model in `embeddings.py` is a local stand-in named as OpenAI's, so nothing
leaves the machine and nothing is charged. With `OPENAI_API_KEY` set and `langchain-openai`
installed, the pipeline calls OpenAI's.

Reports mask every identifier they find, in the page text as well as the findings.
`--reveal` changes that, and says so when it does.

## Command line

| Script | What it runs |
| --- | --- |
| `cli/1-audit.sh` | `complydoc audit` on the folder, and `complydoc sensitive --print-json` on one file |
| `cli/2-compare-loaders.sh` | `complydoc compare-loaders cli/loaders.yaml`: two LangChain loaders on the same files, with an expected fact |
| `cli/3-chunks.sh` | `complydoc chunks` with two chunk sizes of `RecursiveCharacterTextSplitter` |
| `cli/4-diff.sh` | `complydoc diff` against `baseline/report.json`, and its exit code on a regression |
| `cli/5-routing.sh` | `complydoc routing`: the path each page needs, priced as a mix, written as a manifest |

`make cli` runs all five. Reports go to `.complydoc/`, where `complydoc ui` finds them; the
diff and routing outputs, which are for other tools, go to `out/`.

## Python

| Script | API |
| --- | --- |
| `pipeline.py` | `observe`, `StripPathMetadata`, `MaskIdentifiers` around a LangChain pipeline |
| `python/01_audit_a_folder.py` | `full_audit`, `write_json` |
| `python/02_strings.py` | `scan_text`, `mask_text`, `find_hidden`, `count_tokens` |
| `python/03_inspect_a_loader.py` | `inspect_documents` on a LangChain loader |
| `python/04_compare_loaders.py` | `compare_loaders` over files, with a fact and a loader cache |
| `python/05_chunks.py` | `extract_text`, `compare_chunkers` |
| `python/06_pipeline_steps.py` | `StripPathMetadata`, `DropHiddenPassages`, `MaskIdentifiers` on LangChain documents |
| `python/07_baseline_and_diff.py` | `load_report`, `diff_reports` |
| `python/08_extend.py` | `register_detector`, `register_signal`, `Config.override` |
| `python/09_report_tables.py` | `report.to_pandas`, `iter_audit` |

`make python` runs the nine in `python/` from the repository root.

## Policy

`policy.yaml` is the same checks written as rules, for `complydoc check`:

```bash
uv run complydoc check documents --policy policy.yaml --no-ocr
```

It fails on purpose. These samples are built to be found: the questionnaire and the CV
hide instructions to a model in white text, and the invoices, the questionnaire and the
email carry bank details and a card. A folder that passed would show nothing worth reading.
Names are reported as not scanned rather than failing, because this playground installs no
name model.

## Tests and CI

`tests/test_documents.py` uses `cd.expect` to check the documents: nothing regressed
against the baseline, the annual report holds no high-severity identifiers, the hidden
instruction in the questionnaire is caught, and the loader keeps the expected fact and made
no network connection. `make test` runs it.

`.github/workflows/documents.yml` gates the repository two ways, one job each:

- **policy**: the [complydoc action](https://complydoc.github.io/complydoc/docs/guides/github-action/)
  runs `check` against `policy.yaml`, writes the result to the job summary and keeps one
  comment on the pull request up to date. It is set to `fail: false`, so the deliberate
  failures above do not turn the run red; drop that where a failure should stop a merge.
- **baseline**: audits the folder, runs `complydoc diff` against the committed baseline
  (failing on a regression), runs the tests and uploads the reports.

After changing the documents on purpose, `make baseline` rewrites `baseline/report.json`.

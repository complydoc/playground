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
`PyMuPDF4LLMLoader`, `OpenDataLoaderPDFLoader`, which needs Java, and `DoclingLoader`,
which brings PyTorch and downloads its models on first use), LangChain text splitters and
pytest, and downloads the model complydoc finds names with (680 MB, once), which runs on
the PyTorch Docling brings. complydoc's own OCR is left out, so the examples run with
`--no-ocr`.

## Start here

```bash
make start
make ui
```

`make start` runs `experiment.py`: four LangChain PDF loaders (`PyPDFLoader`,
`PyMuPDF4LLMLoader`, `OpenDataLoaderPDFLoader` and `DoclingLoader`, set up in
`loaders.py`) over the same files. Then five LangChain text splitters cut the text
(`complydoc chunks --preset common`). `make ui` opens them in your browser:

- **Documents**: the loaders side by side, and the files they read differently. Open one
  for its Diff against any other loader, line by line, or pick a splitter to see its
  chunks drawn over the text.
- **Chunks**: the splitters side by side, and where their cuts fall.

`make trace` runs `pipeline.py`, a LangChain ingestion pipeline inside `cd.observe`: the
company documents loaded with `PyMuPDF4LLMLoader`, the invoices with `PyPDFLoader`, then
cleaned, split and embedded. It runs twice, as written and with `--mask`, and the Trace
shows every LangChain call with its time, tokens, cost and the identifiers it passed on.
The embedding model in `embeddings.py` is a local stand-in named as OpenAI's, so nothing
leaves the machine and nothing is charged; import `OpenAIEmbeddings` from
`langchain_openai` instead to call OpenAI's.

Reports mask every identifier they find, in the page text as well as the findings.
`--reveal` (`reveal=True` in Python) keeps the values too, and says so when it does; the
loader comparison uses it, so the viewer can unmask these synthetic documents.

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
| `experiment.py` | `compare_loaders`: four LangChain PDF loaders over the same files |
| `python/05_chunks.py` | `extract_text`, `compare_chunkers` |
| `python/06_pipeline_steps.py` | `StripPathMetadata`, `DropHiddenPassages`, `MaskIdentifiers` on LangChain documents |
| `python/07_baseline_and_diff.py` | `load_report`, `diff_reports` |
| `python/08_extend.py` | `register_detector`, `register_signal`, `Config.override` |
| `python/09_report_tables.py` | `report.to_pandas`, `iter_audit` |

`make python` runs the eight in `python/` from the repository root.

## Policy

`policy.yaml` is the same checks written as rules, for `complydoc check`:

```bash
uv run complydoc check documents --policy policy.yaml --no-ocr
```

It fails on purpose. These samples are built to be found: the questionnaire and the CV
hide instructions to a model in white text, and the invoices, the questionnaire and the
email carry bank details and a card. A folder that passed would show nothing worth reading.
Names are found with the multilingual model complydoc runs on PyTorch.

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

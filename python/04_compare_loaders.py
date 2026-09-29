"""Two LangChain PDF loaders on the same files: which one to use, and where they differ.

Writes `.complydoc/loaders.json`. In `complydoc ui`, Documents puts the loaders side by
side, and a document's Diff shows their two readings line by line. The values found are
kept, so the viewer can show them unmasked: the documents here are synthetic.
"""

import warnings
from functools import partial
from pathlib import Path

# langchain-community prints a notice that it is being sunset; PyPDFLoader still lives there.
warnings.filterwarnings("ignore", category=DeprecationWarning)

from langchain_community.document_loaders import PyPDFLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

import complydoc as cd

report = cd.compare_loaders(
    {
        "PyPDFLoader": PyPDFLoader,
        "PyMuPDF4LLMLoader": partial(PyMuPDF4LLMLoader, use_ocr=False),
    },
    # Absolute paths, so documents are named from documents/, as `complydoc chunks` names them.
    paths=sorted(str(pdf.resolve()) for pdf in Path("documents").rglob("*.pdf")),
    facts=[
        cd.Fact(
            "Evidence may be requested for any answer during the on-site review.",
            document="vendor-due-diligence.pdf",
        )
    ],
    cache_dir=".complydoc/loader-cache",
    reveal=True,
)

comparison = report.loader_comparison
print(comparison.verdict)
print(
    report.to_pandas("loaders")[
        ["loader", "documents", "pages", "characters", "facts_found"]
    ]
)
for difference in comparison.identifier_differences:
    print(
        difference.document,
        difference.label,
        difference.value,
        "found by",
        difference.found_by,
    )

cd.write_json(report, ".complydoc/loaders.json", detail="full")

"""Compare two loaders over several files, with a fact the text should contain."""

from pathlib import Path

from langchain_community.document_loaders import PDFPlumberLoader, PyPDFLoader

import complydoc as cd

report = cd.compare_loaders(
    {"pypdf": PyPDFLoader, "pdfplumber": PDFPlumberLoader},
    paths=[
        "documents/employee-record.pdf",
        "documents/terms-and-conditions.pdf",
        "documents/vendor-assessment.pdf",
    ],
    facts=[
        cd.Fact(
            "Two administrator accounts have no multi-factor authentication",
            document="vendor-assessment.pdf",
        )
    ],
    cache_dir=".complydoc/loader-cache",
)

print(report.to_pandas("loaders")[["loader", "documents", "pages", "characters", "facts_found"]])
for difference in report.loader_comparison.identifier_differences:
    print(difference.document, difference.label, difference.masked, "found by", difference.found_by)

Path("out").mkdir(exist_ok=True)
cd.write_html(report, "out/python-loaders.html")

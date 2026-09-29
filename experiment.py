"""Four LangChain PDF loaders on the same document set"""

from functools import partial
from pathlib import Path

import complydoc as cd
from langchain_community.document_loaders import PyPDFLoader
from langchain_docling import DoclingLoader
from langchain_opendataloader_pdf import OpenDataLoaderPDFLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader

loaders = {
    "PyPDFLoader": PyPDFLoader,
    "PyMuPDF4LLMLoader": partial(PyMuPDF4LLMLoader, use_ocr=False),
    "OpenDataLoaderPDFLoader": partial(OpenDataLoaderPDFLoader, quiet=True),
    "DoclingLoader": DoclingLoader,
}
pdfs = sorted(Path("documents").rglob("*.pdf"))

report = cd.compare_loaders(
    loaders, paths=pdfs, reveal=True, page_images=True, allow_network=True
)
cd.write_json(report, ".complydoc/loaders.json", detail="full")

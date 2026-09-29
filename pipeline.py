"""A LangChain ingestion pipeline, observed by complydoc.

    uv run python pipeline.py          # as written: identifiers reach the model
    uv run python pipeline.py --mask   # with masking added before the split
    uv run complydoc ui                # the traces, side by side

Two sources, each with the LangChain loader that suits it, one splitter and one
embedding model. Every LangChain call inside the block becomes a step of the trace,
with its time, tokens, cost and the identifiers it passed on.
"""

import sys
from pathlib import Path

import complydoc as cd
from langchain_community.document_loaders import PyPDFLoader
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from embeddings import OpenAIEmbeddings

with cd.observe("documents-ingest") as run:
    documents = []
    for pdf in sorted(Path("documents/company").glob("*.pdf")):
        documents += PyMuPDF4LLMLoader(str(pdf), use_ocr=False).load()
    for pdf in sorted(Path("documents/invoices").glob("*.pdf")):
        documents += PyPDFLoader(str(pdf)).load()

    documents = cd.StripPathMetadata().transform_documents(documents)
    if "--mask" in sys.argv:
        documents = cd.MaskIdentifiers().transform_documents(documents)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    OpenAIEmbeddings(model="text-embedding-3-small").embed_documents(
        [chunk.page_content for chunk in chunks]
    )

print(run.summary())

"""Compare chunk sizes on the folder's text with a LangChain splitter."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

import complydoc as cd

text = cd.extract_text("documents", ocr=False, mask=False)
documents = [
    Document(page_content=chunk.text, metadata={"source": chunk.document, "page": chunk.page})
    for chunk in text.chunks
]

comparison = cd.compare_chunkers(
    {
        "300": RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=0),
        "1200": RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=100),
    },
    documents,
    facts=["Two administrator accounts have no multi-factor authentication"],
    max_tokens=400,
)

print(comparison.to_pandas()[["chunker", "chunks", "tokens_median", "split_sentence", "facts_split"]])

small = comparison.reports["300"]
for chunk in small.chunks:
    if "split_sentence" in chunk.flags:
        print(chunk.document, chunk.page, chunk.preview[:70])
        break

cd.write_chunks_html(comparison, "out/python-chunks.html", source="documents")

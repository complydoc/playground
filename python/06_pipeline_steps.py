"""Clean loaded documents before they reach an index: drop absolute paths from
metadata, drop passages addressed to a model, mask identifiers."""

from langchain_community.document_loaders import PyPDFLoader

import complydoc as cd

documents = PyPDFLoader("documents/vendor-assessment.pdf").load()
documents += PyPDFLoader("documents/employee-record.pdf").load()

steps = [cd.StripPathMetadata(), cd.DropHiddenPassages(), cd.MaskIdentifiers()]
for step in steps:
    documents = step.transform_documents(documents)
    for change in step.changes:
        print(f"{change.step:<20} {change.document}: {change.detail}")

print(documents[-1].metadata)
print(documents[-1].page_content[:300])

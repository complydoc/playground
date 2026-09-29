"""Inspect what a LangChain loader returned: text, metadata and network attempts."""

from langchain_community.document_loaders import PyPDFLoader

import complydoc as cd

report = cd.inspect_documents(PyPDFLoader("documents/company/employee-handbook.pdf"))

loader = report.loader
assert loader is not None, "inspect_documents always reports the loader it ran"
print(f"{loader.name}: {loader.documents_returned} documents")
print(f"network attempts: {loader.network_attempts or 'none'}")
print(f"metadata keys: {', '.join(loader.metadata_keys)}")

for document in report.documents:
    print(
        document.relative_path,
        len(document.sensitive.matches) if document.sensitive else 0,
        "identifiers in text",
    )
    for finding in document.metadata_findings:
        print(f"  metadata {finding.key}: {finding.label} {finding.masked}")
    if document.path_exposures:
        print(f"  absolute paths in: {', '.join(document.path_exposures)}")

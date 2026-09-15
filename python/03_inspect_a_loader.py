"""Inspect what a LangChain loader returned: text, metadata and network attempts."""

from langchain_community.document_loaders import PyPDFLoader

import complydoc as cd

report = cd.inspect_documents(PyPDFLoader("documents/employee-record.pdf"))

loader = report.loader
print(f"{loader.name}: {loader.documents_returned} documents")
print(f"network attempts: {loader.network_attempts or 'none'}")
print(f"metadata keys: {', '.join(loader.metadata_keys)}")

for document in report.documents:
    print(document.relative_path, len(document.sensitive.matches), "identifiers in text")
    for finding in document.metadata_findings:
        print(f"  metadata {finding.key}: {finding.label} {finding.masked}")
    if document.path_exposures:
        print(f"  absolute paths in: {', '.join(document.path_exposures)}")

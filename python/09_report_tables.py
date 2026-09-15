"""Read a report as pandas tables, as in a notebook."""

import complydoc as cd

report = cd.full_audit("documents", ocr=False)

print(report.to_pandas("documents")[["document", "readiness_score", "identifiers", "hidden_passages"]])
print(report.to_pandas("identifiers")[["document", "label", "evidence", "value"]].head(10))
print(report.to_pandas("hidden")[["document", "visibility", "instruction", "severity"]])

for document in cd.iter_audit("documents", components=("sensitive",), ocr=False):
    if isinstance(document, cd.DocumentReport):
        print("streamed", document.relative_path, document.sensitive.total)

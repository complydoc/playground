"""Audit a folder and read the results."""

from pathlib import Path

import complydoc as cd

report = cd.full_audit("documents", ocr=False)

print(f"global readiness: {report.overall.score:.0f} ({report.overall.label})")
for document in report.documents:
    identifiers = document.sensitive.total if document.sensitive else 0
    score = document.readiness.score.value if document.readiness and document.readiness.score else None
    print(
        f"{document.relative_path:<28} readiness {score if score is not None else '-':>5}  "
        f"identifiers {identifiers:>3}  hidden passages {len(document.content_findings)}"
    )

for limitation in report.limitations:
    print(f"[{limitation.severity}] {limitation.area}: {limitation.statement}")

Path("out").mkdir(exist_ok=True)
cd.write_html(report, "out/python-audit.html")
cd.write_json(report, "out/python-audit.json")

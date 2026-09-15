"""Compare a new audit with the committed baseline and write the changes as a page."""

from pathlib import Path

import complydoc as cd

baseline = cd.load_report("baseline/report.json")
current = cd.full_audit("documents", ocr=False, page_images=False, extracted_text=False)

changes = cd.diff_reports(baseline, current)
print(changes.summary())

# The same comparison against part of the folder, where documents go missing.
partial = cd.full_audit("documents/employee-record.pdf", ocr=False, extracted_text=False)
partial_changes = cd.diff_reports(baseline, partial)
print(len(partial_changes.regressions), "regressions against one document")

Path("out").mkdir(exist_ok=True)
cd.write_diff_html(partial_changes, "out/python-diff.html", old="baseline", new="one document")

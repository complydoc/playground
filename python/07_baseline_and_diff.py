"""Compare a new audit with the committed baseline, as a CI job does."""

import complydoc as cd

baseline = cd.load_report("baseline/report.json")
current = cd.full_audit("documents", ocr=False, page_images=False, extracted_text=False)

changes = cd.diff_reports(baseline, current)
print(changes.summary())

# The same comparison against part of the folder, where documents go missing.
partial = cd.full_audit("documents/company/employee-handbook.pdf", ocr=False, extracted_text=False)
partial_changes = cd.diff_reports(baseline, partial)
print(len(partial_changes.regressions), "regressions against one document")

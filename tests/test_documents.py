"""Checks on the documents, as a test suite would run them before indexing."""

import pytest
from langchain_community.document_loaders import PyPDFLoader

import complydoc as cd


@pytest.fixture(scope="module")
def report():
    return cd.full_audit("documents", ocr=False, extracted_text=False, page_images=False)


def test_every_file_was_read(report):
    # all_categories_scanned() would fail here: names need the optional `ner` extra.
    cd.expect(report).no_failures()


def test_no_regressions_against_the_baseline(report):
    cd.expect(report).no_regressions("baseline/report.json")


def test_the_terms_hold_no_high_severity_identifiers():
    terms = cd.security_audit("documents/terms-and-conditions.pdf", ocr=False)
    cd.expect(terms).no_identifiers(severity="high").no_hidden(severity="high")


def test_the_hidden_instruction_in_the_vendor_assessment_is_caught():
    vendor = cd.security_audit("documents/vendor-assessment.pdf", ocr=False)
    with pytest.raises(cd.ExpectationError):
        cd.expect(vendor).no_hidden(severity="high")


def test_the_loader_keeps_the_key_fact_and_stays_offline():
    report = cd.inspect_documents(PyPDFLoader("documents/vendor-assessment.pdf"))
    cd.check_facts(report, ["Two administrator accounts have no multi-factor authentication"])
    cd.expect(report).no_network()

"""
Unit Tests for Citation Integrity & Validation (backend/citation_checker.py)
============================================================================
Tests:
1. Successful citations (PMID verified, metadata accurate, relevance >= 0.32, clickable link).
2. Missing citations (factual assertions lacking a cited PMID).
3. Unsupported claims (PMID cited, but cited paper text does not support assertion).
4. Hallucinated PMIDs (citations referencing PMIDs absent from retrieved set).
5. Generation of official clickable PubMed links (https://pubmed.ncbi.nlm.nih.gov/<pmid>/).
"""

import unittest
from backend.citation_checker import (
    extract_citations,
    extract_sentences_with_citations,
    validate_citations_comprehensive,
    verify_citations,
    CitationAuditReport,
    ValidatedCitation,
    UnsupportedClaim,
)
from backend.pubmed import PaperMetadata
from backend.preprocessing import EvidenceChunk


class TestCitationValidation(unittest.TestCase):
    def setUp(self):
        # Authentic source paper 1: Zinc and common cold
        self.paper_zinc = PaperMetadata(
            pmid="23775705",
            title="Zinc for the common cold",
            abstract="Zinc administered within 24 hours of onset of symptoms reduces the duration of common cold symptoms in healthy people.",
            journal="The Cochrane Database of Systematic Reviews",
            year="2013",
            authors=["Singh M", "Das RR"],
            doi="10.1002/14651858.CD001364.pub4"
        )
        self.chunk_zinc = EvidenceChunk(
            chunk_id="23775705_0",
            pmid="23775705",
            title="Zinc for the common cold",
            journal="The Cochrane Database of Systematic Reviews",
            year="2013",
            url="https://pubmed.ncbi.nlm.nih.gov/23775705/",
            text="Zinc administered within 24 hours of onset of symptoms reduces the duration of common cold symptoms in healthy people."
        )

        # Authentic source paper 2: Vitamin D immunity
        self.paper_vitd = PaperMetadata(
            pmid="34322844",
            title="Immunologic effects of vitamin D",
            abstract="Vitamin D modulates both innate and adaptive immune responses, inducing cathelicidin and beta-defensin expression in macrophages.",
            journal="Reviews in Endocrine and Metabolic Disorders",
            year="2022",
            authors=["Charoenngam N", "Holick MF"],
            doi="10.1007/s11154-021-09675-2"
        )
        self.chunk_vitd = EvidenceChunk(
            chunk_id="34322844_0",
            pmid="34322844",
            title="Immunologic effects of vitamin D",
            journal="Reviews in Endocrine and Metabolic Disorders",
            year="2022",
            url="https://pubmed.ncbi.nlm.nih.gov/34322844/",
            text="Vitamin D modulates both innate and adaptive immune responses, inducing cathelicidin and beta-defensin expression in macrophages."
        )

        self.papers = [self.paper_zinc, self.paper_vitd]
        self.chunks = [self.chunk_zinc, self.chunk_vitd]

    def test_extract_citations(self):
        """Test extraction across varied citation formats."""
        text = (
            "Systematic reviews [PMID: 23775705] and observational studies "
            "(PMID 34322844) support these findings. Another is PMID: 12345678."
        )
        pmids = extract_citations(text)
        self.assertEqual(pmids, {"23775705", "34322844", "12345678"})

    def test_successful_citations(self):
        """Test that authentic citations are validated with correct metadata and clickable links."""
        answer = (
            "Administering zinc lozenges early reduces the duration of common cold symptoms [PMID: 23775705]. "
            "Furthermore, vitamin D modulates innate immune responses through cathelicidin induction [PMID: 34322844]."
        )
        report: CitationAuditReport = validate_citations_comprehensive(
            answer_text=answer,
            papers=self.papers,
            chunks=self.chunks,
            relevance_threshold=0.30
        )

        self.assertTrue(report.is_valid)
        self.assertEqual(len(report.hallucinated_pmids), 0)
        self.assertEqual(len(report.verified_citations), 2)

        # Check metadata fidelity
        zinc_cit = next(c for c in report.verified_citations if c.pmid == "23775705")
        self.assertEqual(zinc_cit.url, "https://pubmed.ncbi.nlm.nih.gov/23775705/")
        self.assertEqual(zinc_cit.title, "Zinc for the common cold")
        self.assertEqual(zinc_cit.journal, "The Cochrane Database of Systematic Reviews")
        self.assertEqual(zinc_cit.year, "2013")
        self.assertIn("Singh M", zinc_cit.authors)
        self.assertTrue(zinc_cit.is_relevant)
        self.assertGreaterEqual(zinc_cit.relevance_score, 0.30)

        vitd_cit = next(c for c in report.verified_citations if c.pmid == "34322844")
        self.assertEqual(vitd_cit.url, "https://pubmed.ncbi.nlm.nih.gov/34322844/")
        self.assertTrue(vitd_cit.is_relevant)

    def test_detect_hallucinated_citations(self):
        """Test detection of an invented PMID that was never retrieved from PubMed."""
        answer = (
            "Zinc helps reduce colds [PMID: 23775705]. "
            "An invented study claims megadoses cure all viral infections [PMID: 99999999]."
        )
        report: CitationAuditReport = validate_citations_comprehensive(
            answer_text=answer,
            papers=self.papers,
            chunks=self.chunks
        )

        self.assertFalse(report.is_valid)
        self.assertIn("99999999", report.hallucinated_pmids)
        self.assertNotIn("23775705", report.hallucinated_pmids)

    def test_detect_missing_citations(self):
        """Test identification of substantive factual claims that lack a PMID source reference."""
        answer = (
            "Administering zinc lozenges early reduces cold symptom duration [PMID: 23775705].\n\n"
            "Multiple randomized trials have demonstrated that high-dose intravenous therapy reduces infection risk in hospitalized patients."
        )
        report: CitationAuditReport = validate_citations_comprehensive(
            answer_text=answer,
            papers=self.papers,
            chunks=self.chunks
        )

        self.assertGreaterEqual(len(report.missing_citations), 1)
        self.assertTrue(any("intravenous therapy" in s for s in report.missing_citations))

    def test_detect_unsupported_claim(self):
        """Test that a claim citing an authentic PMID is flagged as unsupported if the content doesn't match."""
        # Citing the Zinc paper for a completely unrelated assertion about Metformin / diabetes
        answer = (
            "Metformin significantly reduces HbA1c and improves insulin sensitivity in diabetic adults [PMID: 23775705]."
        )
        report: CitationAuditReport = validate_citations_comprehensive(
            answer_text=answer,
            papers=self.papers,
            chunks=self.chunks,
            relevance_threshold=0.32
        )

        # The PMID is in the retrieved set (not hallucinated), but the paper doesn't support the claim
        self.assertTrue(report.is_valid)  # No hallucinated PMIDs
        self.assertGreaterEqual(len(report.unsupported_claims), 1)
        unsupported = report.unsupported_claims[0]
        self.assertEqual(unsupported.cited_pmid, "23775705")
        self.assertLess(unsupported.relevance_score, 0.32)
        self.assertIn("low semantic relevance", unsupported.reason.lower())

    def test_legacy_verify_citations(self):
        """Test backward compatibility of verify_citations helper."""
        text = "Zinc lozenges [PMID: 23775705] and fake paper [PMID: 88888888]."
        verified, hallucinated, available = verify_citations(text, self.chunks)
        self.assertEqual(verified, {"23775705"})
        self.assertEqual(hallucinated, {"88888888"})
        self.assertEqual(available, {"23775705", "34322844"})


if __name__ == "__main__":
    unittest.main()

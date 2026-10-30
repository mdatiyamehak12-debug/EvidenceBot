"""
Unit Tests for Scientific Abstention Mechanism (backend/evidence_checker.py & backend/rag_pipeline.py)
=====================================================================================================
Tests all 5 Scientific Abstention triggers:
1. No relevant papers retrieved from PubMed.
2. Retrieved abstracts do not contain enough information (empty abstracts).
3. The evidence does not address the question (top similarity < threshold / irrelevant papers).
4. Evidence is conflicting.
5. Claims cannot be linked to reliable supporting passages.
6. Validation of exact abstention message and structured diagnostic payload.
"""

import unittest
from backend.evidence_checker import (
    evaluate_abstention_triggers,
    AbstentionReport,
    VerifiedClaim,
    EvidenceStatus,
)
from backend.pubmed import PaperMetadata
from backend.preprocessing import EvidenceChunk
from utils import config


class TestAbstentionMechanism(unittest.TestCase):
    def setUp(self):
        self.exact_required_message = (
            "I could not find sufficient reliable evidence in the retrieved literature to provide a confident answer."
        )

    def test_standard_abstention_message_matches_requirement(self):
        """Verifies that the configuration and default AbstentionReport match the exact required string."""
        self.assertEqual(config.ABSTENTION_MESSAGE, self.exact_required_message)
        report = AbstentionReport(is_abstained=True)
        self.assertEqual(report.standard_message, self.exact_required_message)

    def test_trigger_1_no_papers_retrieved(self):
        """Trigger 1: Zero papers returned by PubMed search."""
        query = "ObscureNonExistentCompound999 mechanism"
        report = evaluate_abstention_triggers(
            search_query=query,
            papers=[],
            chunks=[],
            top_similarity_score=0.0,
            threshold=0.32
        )

        self.assertIsNotNone(report)
        self.assertTrue(report.is_abstained)
        self.assertEqual(report.standard_message, self.exact_required_message)
        self.assertEqual(report.search_query, query)
        self.assertEqual(report.papers_retrieved_count, 0)
        self.assertIn("No peer-reviewed publications", report.reason)
        self.assertTrue(len(report.additional_research_required) > 0)

    def test_trigger_2_empty_abstracts(self):
        """Trigger 2: Retrieved PubMed papers have no usable abstract content."""
        query = "Some hypothetical biomarker in rare syndrome"
        title_only_papers = [
            PaperMetadata(pmid="11111111", title="Title only without abstract", abstract="")
        ]
        report = evaluate_abstention_triggers(
            search_query=query,
            papers=title_only_papers,
            chunks=[],  # No chunks produced because abstract was empty
            top_similarity_score=0.0,
            threshold=0.32
        )

        self.assertIsNotNone(report)
        self.assertTrue(report.is_abstained)
        self.assertEqual(report.search_query, query)
        self.assertEqual(report.papers_retrieved_count, 1)
        self.assertIn("lack structured abstract text", report.reason)

    def test_trigger_3_irrelevant_papers_low_similarity(self):
        """Trigger 3: Retrieved papers do not address the question (top similarity < threshold)."""
        query = "Does zinc supplementation treat severe Alzheimer's dementia?"
        # Literature on skin dermatology or unrelated topics retrieved
        dummy_papers = [
            PaperMetadata(pmid="22222222", title="Dermatological effects of topical zinc", abstract="Topical zinc reduces minor skin irritation.")
        ]
        dummy_chunks = [
            EvidenceChunk(chunk_id="22222222_0", pmid="22222222", title="Dermatological effects", text="Topical zinc reduces minor skin irritation.", score=0.18)
        ]

        report = evaluate_abstention_triggers(
            search_query=query,
            papers=dummy_papers,
            chunks=dummy_chunks,
            top_similarity_score=0.18,
            threshold=0.32
        )

        self.assertIsNotNone(report)
        self.assertTrue(report.is_abstained)
        self.assertEqual(report.papers_retrieved_count, 1)
        self.assertIn("below our strict confidence threshold", report.reason)
        self.assertIn("Targeted interventional trials", report.additional_research_required)

    def test_trigger_4_conflicting_evidence(self):
        """Trigger 4: Literature presents conflicting or contradicted findings."""
        query = "Does Herbal Extract Z prevent viral infections?"
        dummy_papers = [
            PaperMetadata(pmid="33333333", title="Trial of Extract Z", abstract="Extract Z showed no benefit.")
        ]
        dummy_chunks = [
            EvidenceChunk(chunk_id="33333333_0", pmid="33333333", title="Trial of Extract Z", text="Extract Z showed no benefit.", score=0.55)
        ]
        # Verified claims show contradiction
        contradicted_claim = VerifiedClaim(
            claim_id=1,
            claim_text="Herbal Extract Z prevents viral infections.",
            status=EvidenceStatus.CONTRADICTED,
            confidence_score=0.55,
            matched_pmid="33333333",
            matched_paper_title="Trial of Extract Z",
            matched_excerpt="Extract Z showed no benefit.",
            matched_url="https://pubmed.ncbi.nlm.nih.gov/33333333/",
            reason="Trial demonstrates lack of effect.",
            study_type="Randomized Controlled Trial (Human RCT)"
        )

        report = evaluate_abstention_triggers(
            search_query=query,
            papers=dummy_papers,
            chunks=dummy_chunks,
            top_similarity_score=0.55,
            threshold=0.32,
            verified_claims=[contradicted_claim]
        )

        self.assertIsNotNone(report)
        self.assertTrue(report.is_abstained)
        self.assertIn("conflicting or null-effect findings", report.reason)
        self.assertIn("systematic review and meta-analysis", report.additional_research_required)

    def test_trigger_5_claims_cannot_be_linked_to_passages(self):
        """Trigger 5: Factual claims cannot be substantiated by verified literature."""
        query = "Specific metabolic pathway mechanism"
        dummy_papers = [
            PaperMetadata(pmid="44444444", title="General metabolic review", abstract="General overview.")
        ]
        dummy_chunks = [
            EvidenceChunk(chunk_id="44444444_0", pmid="44444444", title="General review", text="General overview.", score=0.42)
        ]
        unsupported_claim = VerifiedClaim(
            claim_id=1,
            claim_text="Compound activates Receptor Q directly.",
            status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
            confidence_score=0.20,
            matched_pmid=None,
            matched_paper_title=None,
            matched_excerpt=None,
            matched_url=None,
            reason="Retrieved text does not mention Receptor Q.",
            study_type="Biomedical Literature"
        )

        report = evaluate_abstention_triggers(
            search_query=query,
            papers=dummy_papers,
            chunks=dummy_chunks,
            top_similarity_score=0.42,
            threshold=0.32,
            verified_claims=[unsupported_claim]
        )

        self.assertIsNotNone(report)
        self.assertTrue(report.is_abstained)
        self.assertIn("could not be linked to reliable, verified supporting passages", report.reason)

    def test_no_abstention_when_evidence_is_sufficient(self):
        """When evidence is high quality, relevant, and supported, no abstention should be triggered."""
        query = "Role of vitamin D in immunity"
        dummy_papers = [
            PaperMetadata(pmid="34322844", title="Vitamin D in immunity", abstract="Vitamin D enhances cathelicidin expression.")
        ]
        dummy_chunks = [
            EvidenceChunk(chunk_id="34322844_0", pmid="34322844", title="Vitamin D in immunity", text="Vitamin D enhances cathelicidin expression.", score=0.68)
        ]
        supported_claim = VerifiedClaim(
            claim_id=1,
            claim_text="Vitamin D enhances antimicrobial peptides like cathelicidin.",
            status=EvidenceStatus.SUPPORTED,
            confidence_score=0.68,
            matched_pmid="34322844",
            matched_paper_title="Vitamin D in immunity",
            matched_excerpt="Vitamin D enhances cathelicidin expression.",
            matched_url="https://pubmed.ncbi.nlm.nih.gov/34322844/",
            reason="Direct textual support found.",
            study_type="Randomized Controlled Trial (Human RCT)"
        )

        report = evaluate_abstention_triggers(
            search_query=query,
            papers=dummy_papers,
            chunks=dummy_chunks,
            top_similarity_score=0.68,
            threshold=0.32,
            verified_claims=[supported_claim]
        )

        self.assertIsNone(report)


if __name__ == "__main__":
    unittest.main()


"""
Unit Tests for Evidence Checker Module (backend/evidence_checker.py)
"""

import unittest
from backend.preprocessing import EvidenceChunk
from backend.evidence_checker import (
    extract_claims_from_answer,
    detect_study_type,
    check_causation_overstatement,
    detect_contradiction,
    verify_answer_claims,
    EvidenceStatus
)


class TestEvidenceChecker(unittest.TestCase):
    def setUp(self):
        self.chunk_rct = EvidenceChunk(
            chunk_id="34322844_0",
            pmid="34322844",
            title="Randomized Trial of Vitamin D",
            journal="Reviews in Endocrine Disorders",
            year="2022",
            url="https://pubmed.ncbi.nlm.nih.gov/34322844/",
            text="In a randomized double-blind clinical trial, vitamin D supplementation reduced respiratory infection rates significantly."
        )
        self.chunk_obs = EvidenceChunk(
            chunk_id="36857810_0",
            pmid="36857810",
            title="Observational Cohort Study on Immunity",
            journal="Paediatrics and International Child Health",
            year="2023",
            url="https://pubmed.ncbi.nlm.nih.gov/36857810/",
            text="A prospective cohort study observed that low serum vitamin D status is associated with higher infection rates."
        )
        self.chunk_null = EvidenceChunk(
            chunk_id="11111111_0",
            pmid="11111111",
            title="Trial of Herbal Extract X",
            journal="Phytomedicine",
            year="2021",
            url="https://pubmed.ncbi.nlm.nih.gov/11111111/",
            text="Extract X failed to show any significant difference and did not reduce symptom duration compared to placebo."
        )

    def test_extract_claims_from_answer(self):
        sample_answer = """
        ### 🎯 Direct Answer
        Vitamin D plays an active role in immune function by stimulating antimicrobial peptides [PMID: 34322844].

        ### 🔬 Supporting Evidence
        - Randomized trials indicate that oral supplementation decreases infection rates.
        - Observational cohorts report that deficient individuals suffer more frequent viral illnesses.
        """
        claims = extract_claims_from_answer(sample_answer)
        self.assertTrue(len(claims) >= 2)
        # Should not include the header "### 🎯 Direct Answer" as a claim
        for c in claims:
            self.assertFalse(c.startswith("#"))

    def test_detect_study_type(self):
        self.assertEqual(
            detect_study_type("In a randomized double-blind placebo-controlled clinical trial"),
            "Randomized Controlled Trial (Human RCT)"
        )
        self.assertEqual(
            detect_study_type("A prospective observational cohort study was conducted on 500 patients"),
            "Observational Study (Cohort/Epidemiological)"
        )
        self.assertEqual(
            detect_study_type("In vitro cell culture assays using isolated human macrophages"),
            "Laboratory In-Vitro / Molecular Study"
        )
        self.assertEqual(
            detect_study_type("Murine models and mice were injected with the pathogen"),
            "Preclinical Animal Model (In-Vivo)"
        )

    def test_check_causation_overstatement(self):
        # Claim states direct causation
        causal_claim = "Vitamin D directly causes the cure of viral pneumonia."
        # Study is observational
        is_overstatement = check_causation_overstatement(
            causal_claim,
            self.chunk_obs.text,
            "Observational Study (Cohort/Epidemiological)"
        )
        self.assertTrue(is_overstatement)

    def test_detect_contradiction(self):
        positive_claim = "Extract X significantly reduces cold symptoms and improves recovery."
        contradicted = detect_contradiction(positive_claim, self.chunk_null.text)
        self.assertTrue(contradicted)

    def test_verify_answer_claims_classification(self):
        answer = "Vitamin D supplementation reduced respiratory infection rates significantly [PMID: 34322844]."
        verified = verify_answer_claims(answer, [self.chunk_rct])
        self.assertEqual(len(verified), 1)
        v = verified[0]
        self.assertIn(v.status, [EvidenceStatus.SUPPORTED, EvidenceStatus.PARTIALLY_SUPPORTED])
        self.assertEqual(v.matched_pmid, "34322844")
        self.assertTrue(v.is_abstract_only)
        self.assertIn("Randomized Controlled Trial", v.study_type)


if __name__ == "__main__":
    unittest.main()


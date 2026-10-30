"""
Unit Tests for LLM Integration (backend/llm.py)
"""

import unittest
from backend.preprocessing import EvidenceChunk
from backend.llm import (
    BIOMEDICAL_SYSTEM_PROMPT,
    format_context_for_llm,
    extractive_fallback_synthesizer,
    generate_biomedical_answer,
)


class TestLLMIntegration(unittest.TestCase):
    def setUp(self):
        self.chunks = [
            EvidenceChunk(
                chunk_id="34322844_chunk_0",
                pmid="34322844",
                title="Vitamin D, infections and immunity",
                journal="Reviews in endocrine & metabolic disorders",
                year="2022",
                url="https://pubmed.ncbi.nlm.nih.gov/34322844/",
                text="Vitamin D regulates innate immune responses to pathogens by inducing antimicrobial peptides.",
                score=0.82
            )
        ]

    def test_system_prompt_guardrails(self):
        """Verifies critical scientific & ethical constraints are in the system prompt."""
        self.assertIn("STRICT EVIDENCE GROUNDING", BIOMEDICAL_SYSTEM_PROMPT)
        self.assertIn("ZERO CITATION HALLUCINATION", BIOMEDICAL_SYSTEM_PROMPT)
        self.assertIn("DISTINGUISH CORRELATION VS. CAUSATION", BIOMEDICAL_SYSTEM_PROMPT)
        self.assertIn("NO PERSONAL MEDICAL ADVICE", BIOMEDICAL_SYSTEM_PROMPT)
        self.assertIn("HONEST ABSTENTION", BIOMEDICAL_SYSTEM_PROMPT)

    def test_context_formatting(self):
        context = format_context_for_llm(self.chunks)
        self.assertIn("PMID: 34322844", context)
        self.assertIn("Vitamin D, infections and immunity", context)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34322844/", context)

    def test_answer_format_sections(self):
        """Verifies that the generated synthesis adheres to all 6 required headings."""
        answer = extractive_fallback_synthesizer("What is the role of vitamin D in immunity?", self.chunks)
        
        required_headings = [
            "### 🎯 Direct Answer",
            "### 📋 Summary of Findings",
            "### 🔬 Supporting Evidence",
            "### ⚖️ Contradicting or Conflicting Findings",
            "### ⚠️ Limitations & Scientific Uncertainty",
            "### 📚 Citations",
        ]
        for heading in required_headings:
            self.assertIn(heading, answer, f"Missing required heading: {heading}")

        # Check citations
        self.assertIn("[PMID: 34322844]", answer)
        self.assertIn("https://pubmed.ncbi.nlm.nih.gov/34322844/", answer)

    def test_generate_biomedical_answer_empty(self):
        res = generate_biomedical_answer("test question", [])
        self.assertTrue(res["is_abstention"])


if __name__ == "__main__":
    unittest.main()


"""
Unit & Integration Tests for RAG Pipeline (backend/rag_pipeline.py)
Tests text chunking, FAISS vector indexing, similarity retrieval,
abstention guards, and citation provenance.
"""

import unittest
from backend.pubmed import PaperMetadata, SearchResult
from backend.rag_pipeline import run_rag_pipeline


class MockPubMedRetriever:
    """Mock retriever returning authentic PubMed records for offline testing."""
    def __init__(self, papers):
        self.papers = papers

    def retrieve(self, query: str, max_results: int = 5) -> SearchResult:
        if "xyzempty" in query:
            return SearchResult(query=query, total_found=0, pmids=[], papers=[], is_empty=True)
        return SearchResult(
            query=query,
            total_found=len(self.papers),
            pmids=[p.pmid for p in self.papers],
            papers=self.papers,
            is_empty=False
        )


class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        # Real PubMed records from NCBI
        self.real_papers = [
            PaperMetadata(
                pmid="34322844",
                title="Vitamin D, infections and immunity",
                journal="Reviews in endocrine & metabolic disorders",
                year="2022",
                authors=["Aiten Ismailova", "John H White"],
                doi="10.1007/s11154-021-09679-5",
                abstract=(
                    "Vitamin D, best known for its role in skeletal health, has emerged as a key regulator "
                    "of innate immune responses to microbial threat. In immune cells such as macrophages, "
                    "expression of CYP27B1 converts 25-hydroxyvitamin D into active 1,25-dihydroxyvitamin D, "
                    "inducing antimicrobial peptides like cathelicidin to combat pathogens."
                ),
                has_abstract=True
            ),
            PaperMetadata(
                pmid="23857223",
                title="Vitamin D and immune function",
                journal="Nutrients",
                year="2013",
                authors=["Barbara Prietl", "Gerlies Treiber"],
                doi="10.3390/nu5072502",
                abstract=(
                    "Vitamin D metabolizing enzymes and vitamin D receptors are present in many cell types "
                    "including various immune cells such as antigen-presenting cells, T cells, B cells and monocytes. "
                    "In vitro data show that vitamin D modulates T cell proliferation and reduces inflammatory cytokine production."
                ),
                has_abstract=True
            ),
            # Paper with missing abstract to verify it is filtered out
            PaperMetadata(
                pmid="99999999",
                title="Editorial Comment on Endocrinology",
                journal="Journal of Endocrinology",
                year="2021",
                authors=["Editor Doe"],
                doi=None,
                abstract="No abstract available in the official PubMed record.",
                has_abstract=False
            )
        ]
        self.mock_retriever = MockPubMedRetriever(self.real_papers)

    def test_rag_pipeline_successful_retrieval(self):
        question = "What is the role of vitamin D in immunity and T cells?"
        result = run_rag_pipeline(
            question=question,
            threshold=0.30,
            retriever=self.mock_retriever
        )

        self.assertEqual(result["status"], "success")
        self.assertFalse(result["is_abstention"])
        self.assertTrue(result["max_score"] >= 0.30)
        self.assertTrue(len(result["chunks"]) > 0)

        # Check metadata provenance
        first_chunk = result["chunks"][0]
        self.assertIn(first_chunk.pmid, {"34322844", "23857223"})
        self.assertNotEqual(first_chunk.pmid, "99999999")  # Missing abstract was excluded!
        self.assertTrue(first_chunk.url.startswith("https://pubmed.ncbi.nlm.nih.gov/"))
        self.assertIsNotNone(first_chunk.score)

        # Verify synthesized answer contains citations
        self.assertIn("PMID:", result["answer"])

    def test_rag_pipeline_abstains_on_irrelevant_query(self):
        """Tests that EvidenceBot refuses to use irrelevant documents."""
        irrelevant_question = "How do you bake a sourdough bread loaf with yeast?"
        result = run_rag_pipeline(
            question=irrelevant_question,
            threshold=0.40,
            retriever=self.mock_retriever
        )

        # Pipeline must recognize similarity is too low and abstain!
        self.assertEqual(result["status"], "abstained")
        self.assertTrue(result["is_abstention"])
        self.assertEqual(result["confidence"], "Insufficient")
        self.assertIn("Scientific Abstention", result["answer"])


if __name__ == "__main__":
    unittest.main()


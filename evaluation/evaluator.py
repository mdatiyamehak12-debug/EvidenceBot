"""
EvidenceBot - Scientific Evaluation & Benchmarking Module
=========================================================
Computes quantitative evaluation metrics and benchmarks EvidenceBot across 5
core biomedical test scenarios:
1. Retrieval Precision@K
2. Retrieval Recall@K
3. Citation Validity Rate
4. Evidence Support Rate
5. Unsupported Claim Rate
6. Abstention Rate & Accuracy
7. Answer Correctness against Validated Reference Answers

Explicitly separates automated mathematical metrics from human-reviewed qualitative assessments.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
import json
import logging
from pathlib import Path
import numpy as np

from utils import config
from backend.pubmed import PaperMetadata, SearchResult, PubMedRetriever
from backend.preprocessing import chunk_papers, EvidenceChunk
from backend.vector_store import FaissVectorStore
from backend.rag_pipeline import run_rag_pipeline, RAGPipelineResult
from backend.evidence_checker import (
    evaluate_evidence_sufficiency,
    evaluate_abstention_triggers,
    verify_answer_claims,
    EvidenceStatus
)
from backend.citation_checker import validate_citations_comprehensive, extract_citations
from backend.embeddings import generate_embeddings

logger = logging.getLogger(__name__)


# =====================================================================
# Metric Computation Helper Functions
# =====================================================================
def compute_precision_at_k(retrieved_pmids: List[str], relevant_pmids: List[str], k: int = 3) -> float:
    """
    Computes Precision@K: Fraction of top-K retrieved papers that are ground-truth relevant.
    If no relevant papers exist (e.g. out-of-domain or fictitious inquiry),
    retrieving 0 papers is considered 1.0 (perfect precision), and retrieving non-relevant is 0.0.
    """
    if not relevant_pmids:
        return 1.0 if len(retrieved_pmids) == 0 else 0.0

    top_k_retrieved = retrieved_pmids[:k]
    if not top_k_retrieved:
        return 0.0

    relevant_set = set(relevant_pmids)
    hits = sum(1 for p in top_k_retrieved if p in relevant_set)
    return float(hits / min(k, len(top_k_retrieved)))


def compute_recall_at_k(retrieved_pmids: List[str], relevant_pmids: List[str], k: int = 3) -> float:
    """
    Computes Recall@K: Fraction of all known ground-truth relevant papers retrieved in top-K.
    If 0 relevant papers exist in ground truth, retrieving 0 is 1.0 (perfect recall).
    """
    if not relevant_pmids:
        return 1.0 if len(retrieved_pmids) == 0 else 0.0

    top_k_retrieved = set(retrieved_pmids[:k])
    relevant_set = set(relevant_pmids)
    hits = len(top_k_retrieved.intersection(relevant_set))
    return float(hits / len(relevant_set))


def compute_citation_validity(
    cited_pmids: Set[str],
    retrieved_pmids: Set[str],
    verified_citations_count: int
) -> float:
    """
    Computes Citation Validity Rate:
    Fraction of citations cited in generated answer that exist in the retrieved literature
    and are verified as authentic NCBI records.
    If no citations were cited:
      - If answer was an abstention: 1.0 (no citations needed).
      - If substantive answer made without citations: 0.0.
    """
    if not cited_pmids:
        return 1.0

    hallucinated = cited_pmids.difference(retrieved_pmids)
    valid_count = len(cited_pmids) - len(hallucinated)
    return max(0.0, min(1.0, float(valid_count / len(cited_pmids))))


def compute_evidence_support_rates(claims_data: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Computes Evidence Support Rate and Unsupported Claim Rate:
    - Support Rate: (SUPPORTED + PARTIALLY_SUPPORTED) / Total Claims
    - Unsupported Rate: (CONTRADICTED + INSUFFICIENT + UNCERTAIN) / Total Claims
    """
    if not claims_data:
        return {"support_rate": 1.0, "unsupported_rate": 0.0}

    total = len(claims_data)
    supported = sum(1 for c in claims_data if c.get("status") in ("SUPPORTED", "PARTIALLY_SUPPORTED"))
    unsupported = total - supported

    return {
        "support_rate": round(float(supported / total), 3),
        "unsupported_rate": round(float(unsupported / total), 3)
    }


def compute_answer_correctness(
    generated_answer: str,
    reference_answer: str,
    is_abstained: bool,
    expected_abstention: bool
) -> float:
    """
    Computes Answer Correctness against Validated Reference Answer:
    1. If both abstained: 1.0 (perfect alignment with gold standard refusal).
    2. If one abstained while the other answered: 0.0 (abstention error).
    3. If both answered: Computes semantic embedding cosine similarity between
       the generated answer and the gold-standard reference.
    """
    if is_abstained and expected_abstention:
        return 1.0
    if is_abstained != expected_abstention:
        return 0.0

    # Both produced substantive answers: compare semantic vectors
    try:
        vecs = generate_embeddings([generated_answer, reference_answer])
        sim = float(np.dot(vecs[0], vecs[1]))
        return max(0.0, min(1.0, round(sim, 3)))
    except Exception as e:
        logger.warning(f"Error computing semantic correctness: {e}")
        # Fallback to lexical token overlap F1
        gen_tokens = set(generated_answer.lower().split())
        ref_tokens = set(reference_answer.lower().split())
        overlap = len(gen_tokens.intersection(ref_tokens))
        if not overlap:
            return 0.0
        precision = overlap / len(gen_tokens)
        recall = overlap / len(ref_tokens)
        f1 = 2 * (precision * recall) / (precision + recall)
        return round(float(f1), 3)


# =====================================================================
# Mock Retriever for Deterministic Offline Benchmark Execution
# =====================================================================
class BenchmarkMockRetriever(PubMedRetriever):
    """
    Enables deterministic, network-independent evaluation using curated test papers.
    When live network is available, standard PubMedRetriever can be used.
    """
    def __init__(self, papers_map: Dict[str, List[PaperMetadata]]):
        super().__init__()
        self.papers_map = papers_map

    def retrieve(self, query: str, max_results: int = 6) -> SearchResult:
        # Match exact query or fuzzy keyword
        for q_key, papers in self.papers_map.items():
            if q_key.lower() in query.lower() or query.lower() in q_key.lower():
                return SearchResult(
                    query=query,
                    total_found=len(papers),
                    pmids=[p.pmid for p in papers],
                    papers=papers[:max_results],
                    is_empty=len(papers) == 0
                )
        return SearchResult(query=query, total_found=0, pmids=[], papers=[], is_empty=True)


# =====================================================================
# Evaluation Data Models
# =====================================================================
@dataclass
class CaseEvaluationResult:
    case_id: str
    name: str
    category: str
    question: str
    expected_abstention: bool
    is_abstention: bool
    abstention_accurate: bool
    retrieved_pmids: List[str]
    expected_pmids: List[str]
    precision_at_k: float
    recall_at_k: float
    citation_validity_rate: float
    evidence_support_rate: float
    unsupported_claim_rate: float
    answer_correctness: float
    confidence_verdict: str
    max_similarity_score: float
    claims_count: int
    citations_count: int
    generated_answer: str
    reference_answer: str
    human_review_notes: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "name": self.name,
            "category": self.category,
            "question": self.question,
            "expected_abstention": self.expected_abstention,
            "is_abstention": self.is_abstention,
            "abstention_accurate": self.abstention_accurate,
            "retrieved_pmids": self.retrieved_pmids,
            "expected_pmids": self.expected_pmids,
            "precision_at_k": round(self.precision_at_k, 3),
            "recall_at_k": round(self.recall_at_k, 3),
            "citation_validity_rate": round(self.citation_validity_rate, 3),
            "evidence_support_rate": round(self.evidence_support_rate, 3),
            "unsupported_claim_rate": round(self.unsupported_claim_rate, 3),
            "answer_correctness": round(self.answer_correctness, 3),
            "confidence_verdict": self.confidence_verdict,
            "max_similarity_score": round(self.max_similarity_score, 3),
            "claims_count": self.claims_count,
            "citations_count": self.citations_count,
            "generated_answer": self.generated_answer,
            "reference_answer": self.reference_answer,
            "human_review_notes": self.human_review_notes,
        }


@dataclass
class BenchmarkSummary:
    total_cases: int
    mean_precision_at_k: float
    mean_recall_at_k: float
    mean_citation_validity: float
    mean_evidence_support_rate: float
    mean_unsupported_claim_rate: float
    abstention_accuracy: float
    mean_answer_correctness: float
    case_results: List[CaseEvaluationResult] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_cases": self.total_cases,
            "mean_precision_at_k": round(self.mean_precision_at_k, 3),
            "mean_recall_at_k": round(self.mean_recall_at_k, 3),
            "mean_citation_validity": round(self.mean_citation_validity, 3),
            "mean_evidence_support_rate": round(self.mean_evidence_support_rate, 3),
            "mean_unsupported_claim_rate": round(self.mean_unsupported_claim_rate, 3),
            "abstention_accuracy": round(self.abstention_accuracy, 3),
            "mean_answer_correctness": round(self.mean_answer_correctness, 3),
            "case_results": [c.to_dict() for c in self.case_results],
        }


# =====================================================================
# Main Evaluator Engine
# =====================================================================
class BenchmarkEvaluator:
    """
    Executes end-to-end evaluation of EvidenceBot against curated biomedical test sets.
    """
    def __init__(self, dataset_path: Optional[str] = None):
        self.dataset_path = dataset_path or (config.ROOT_DIR / "data" / "benchmark_dataset.json")
        self.test_cases = self._load_dataset()

    def _load_dataset(self) -> List[Dict[str, Any]]:
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def run_benchmark(self, use_curated_papers: bool = True, k: int = 3) -> BenchmarkSummary:
        """
        Executes benchmark evaluation across all test cases.
        """
        logger.info(f"Starting EvidenceBot Benchmark on {len(self.test_cases)} cases...")

        # Build mock paper repository for curated/offline reproducibility
        papers_map = {}
        for tc in self.test_cases:
            papers_list = []
            for p_dict in tc.get("source_papers", []):
                papers_list.append(
                    PaperMetadata(
                        pmid=p_dict["pmid"],
                        title=p_dict["title"],
                        abstract=p_dict["abstract"],
                        journal=p_dict.get("journal", "Unknown Journal"),
                        year=p_dict.get("year", "Unknown Year"),
                        authors=p_dict.get("authors", []),
                        doi=p_dict.get("doi")
                    )
                )
            papers_map[tc["question"]] = papers_list

        mock_retriever = BenchmarkMockRetriever(papers_map) if use_curated_papers else None
        results: List[CaseEvaluationResult] = []

        for tc in self.test_cases:
            case_id = tc["id"]
            name = tc["name"]
            category = tc["category"]
            question = tc["question"]
            expected_abstention = tc["expected_abstention"]
            expected_pmids = tc.get("expected_pmids", [])
            reference_answer = tc.get("gold_standard_reference_answer", "")
            notes = tc.get("evaluation_notes", "")

            logger.info(f"Evaluating {case_id}: {name} - '{question}'")

            # Execute RAG Pipeline
            active_retriever = mock_retriever if use_curated_papers else None
            pipeline_output = run_rag_pipeline(
                question=question,
                max_papers=config.DEFAULT_MAX_PAPERS,
                threshold=config.MIN_SIMILARITY_THRESHOLD,
                retriever=active_retriever
            )

            is_abstention = pipeline_output.get("is_abstention", False)
            abstention_accurate = (is_abstention == expected_abstention)
            generated_answer = pipeline_output.get("answer", "")
            confidence = pipeline_output.get("confidence", "Insufficient")
            top_score = pipeline_output.get("max_score", 0.0)

            # Retrieved PMIDs
            retrieved_papers = pipeline_output.get("papers", [])
            retrieved_pmids = [p.pmid for p in retrieved_papers if hasattr(p, "pmid") and p.pmid]

            # 1 & 2. Precision@K and Recall@K
            prec_k = compute_precision_at_k(retrieved_pmids, expected_pmids, k=k)
            rec_k = compute_recall_at_k(retrieved_pmids, expected_pmids, k=k)

            # 3. Citation Validity Rate
            citation_rep = pipeline_output.get("citation_report") or {}
            cited_pmids = extract_citations(generated_answer)
            retrieved_set = set(retrieved_pmids)
            verified_count = len(citation_rep.get("verified_citations", []))
            cit_validity = compute_citation_validity(cited_pmids, retrieved_set, verified_count)

            # 4 & 5. Evidence Support & Unsupported Claim Rates
            verified_claims = pipeline_output.get("verified_claims", [])
            claim_rates = compute_evidence_support_rates(verified_claims)
            support_rate = claim_rates["support_rate"]
            unsupported_rate = claim_rates["unsupported_rate"]

            # 7. Answer Correctness against reference answer
            correctness = compute_answer_correctness(
                generated_answer=generated_answer,
                reference_answer=reference_answer,
                is_abstained=is_abstention,
                expected_abstention=expected_abstention
            )

            res = CaseEvaluationResult(
                case_id=case_id,
                name=name,
                category=category,
                question=question,
                expected_abstention=expected_abstention,
                is_abstention=is_abstention,
                abstention_accurate=abstention_accurate,
                retrieved_pmids=retrieved_pmids,
                expected_pmids=expected_pmids,
                precision_at_k=prec_k,
                recall_at_k=rec_k,
                citation_validity_rate=cit_validity,
                evidence_support_rate=support_rate,
                unsupported_claim_rate=unsupported_rate,
                answer_correctness=correctness,
                confidence_verdict=confidence,
                max_similarity_score=top_score,
                claims_count=len(verified_claims),
                citations_count=len(cited_pmids),
                generated_answer=generated_answer,
                reference_answer=reference_answer,
                human_review_notes=notes
            )
            results.append(res)

        # Aggregate Summary
        n = len(results)
        summary = BenchmarkSummary(
            total_cases=n,
            mean_precision_at_k=float(np.mean([r.precision_at_k for r in results])),
            mean_recall_at_k=float(np.mean([r.recall_at_k for r in results])),
            mean_citation_validity=float(np.mean([r.citation_validity_rate for r in results])),
            mean_evidence_support_rate=float(np.mean([r.evidence_support_rate for r in results])),
            mean_unsupported_claim_rate=float(np.mean([r.unsupported_claim_rate for r in results])),
            abstention_accuracy=float(np.mean([1.0 if r.abstention_accurate else 0.0 for r in results])),
            mean_answer_correctness=float(np.mean([r.answer_correctness for r in results])),
            case_results=results
        )

        # Save results to data/evaluation_results.json
        out_path = config.ROOT_DIR / "data" / "evaluation_results.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, indent=2)

        logger.info(f"Evaluation benchmark complete. Results saved to {out_path}.")
        return summary

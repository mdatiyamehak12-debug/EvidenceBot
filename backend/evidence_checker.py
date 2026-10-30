"""
EvidenceBot - Evidence Verification & Claim Fact-Checking Engine
================================================================
Audits individual factual claims in generated answers against retrieved
scientific literature to evaluate empirical support, contradiction, or insufficiency.

Key Scientific Verification Principles:
1. Claim-Level Decomposition: Breaks answers into atomic factual assertions.
2. Semantic Passage Alignment: Locates exact retrieved passages and PMIDs.
3. 5-Tier Classification:
   - SUPPORTED: Direct empirical backing in the retrieved passage.
   - PARTIALLY SUPPORTED: Evidence supports only part of the claim, or has methodological limits.
   - CONTRADICTED: Retrieved findings directly conflict with the claim.
   - INSUFFICIENT EVIDENCE: Literature does not provide adequate facts to assess the assertion.
   - UNCERTAIN / HUMAN REVIEW: Complex or ambiguous claims that require clinical expert appraisal.
4. Correlation vs. Causation Guard: Detects when a claim asserts definitive causality
   while the supporting study is merely observational or preclinical.
5. Study Type Awareness: Differentiates Clinical Trials (RCTs), Observational Studies,
   Animal Models, and In-Vitro cell experiments.
6. Abstract-Only Scope: Explicitly documents when evidence is synthesized from abstract records.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
import re
import logging
import numpy as np

from utils import config
from utils.helpers import format_pubmed_url
from backend.preprocessing import EvidenceChunk, split_sentences, clean_text
from backend.embeddings import generate_embeddings
from backend.pubmed import PaperMetadata

logger = logging.getLogger(__name__)


# =====================================================================
# Data Structures
# =====================================================================
class EvidenceStatus:
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    UNCERTAIN_HUMAN_REVIEW = "UNCERTAIN_HUMAN_REVIEW"


@dataclass
class AbstentionReport:
    """
    Structured payload detailing a scientific abstention event.
    Guarantees transparent reporting of search scope, retrieved volume,
    failure rationale, and suggested future clinical research.
    """
    is_abstained: bool
    standard_message: str = "I could not find sufficient reliable evidence in the retrieved literature to provide a confident answer."
    search_query: str = ""
    papers_retrieved_count: int = 0
    reason: str = ""
    additional_research_required: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_abstained": self.is_abstained,
            "standard_message": self.standard_message,
            "search_query": self.search_query,
            "papers_retrieved_count": self.papers_retrieved_count,
            "reason": self.reason,
            "additional_research_required": self.additional_research_required,
        }


@dataclass
class VerifiedClaim:
    """
    Detailed audit record for a single factual assertion from an AI answer.
    """
    claim_id: int
    claim_text: str
    status: str                                  # SUPPORTED, PARTIALLY_SUPPORTED, CONTRADICTED, etc.
    confidence_score: float                      # Semantic similarity score (0.0 to 1.0)
    matched_pmid: Optional[str]                  # PMID of best supporting passage
    matched_paper_title: Optional[str]           # Title of source study
    matched_excerpt: Optional[str]               # Exact raw text from abstract
    matched_url: Optional[str]                   # Direct PubMed link
    reason: str                                  # Clear scientific explanation for this status
    study_type: str                              # Inferred study design (RCT, Observational, In-Vitro, etc.)
    has_causal_overstatement: bool = False       # True if correlation stated as direct causation
    is_abstract_only: bool = True                # Flag highlighting abstract-level limitation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_text": self.claim_text,
            "status": self.status,
            "confidence_score": round(self.confidence_score, 3),
            "matched_pmid": self.matched_pmid,
            "matched_paper_title": self.matched_paper_title,
            "matched_excerpt": self.matched_excerpt,
            "matched_url": self.matched_url,
            "reason": self.reason,
            "study_type": self.study_type,
            "has_causal_overstatement": self.has_causal_overstatement,
            "is_abstract_only": self.is_abstract_only,
        }


# =====================================================================
# 1. Claim Extraction Helper
# =====================================================================
def extract_claims_from_answer(answer_text: str) -> List[str]:
    """
    Deconstructs a synthesized Markdown answer into individual factual claims.
    Filters out Markdown structural headers, bullet markers, and disclaimers.
    """
    if not answer_text:
        return []

    raw_lines = answer_text.split("\n")
    candidate_sentences: List[str] = []

    for line in raw_lines:
        line_str = line.strip()
        # Skip section headers, divider lines, and meta headers
        if not line_str or line_str.startswith("#") or line_str.startswith("---") or line_str.startswith("==="):
            continue
        # Skip disclaimers or citation link blocks
        if "disclaimer" in line_str.lower() or line_str.startswith("http"):
            continue

        # Remove leading bullet points or bold prefixes
        cleaned_line = re.sub(r"^[-*•\d.]+\s+", "", line_str).strip()
        if not cleaned_line or len(cleaned_line) < 30:
            continue

        # Split line into sentences
        sentences = split_sentences(cleaned_line)
        for s in sentences:
            s_clean = s.strip()
            # Retain sentences that contain medical/factual assertions
            if len(s_clean) >= 35 and not s_clean.lower().startswith("based on"):
                candidate_sentences.append(s_clean)

    # If extraction found very few sentences, use split_sentences directly on the clean body
    if not candidate_sentences:
        candidate_sentences = [
            s for s in split_sentences(clean_text(answer_text))
            if len(s) >= 40 and not s.startswith("#")
        ]

    return candidate_sentences[:10]  # Cap at top 10 claims for focused evaluation


# =====================================================================
# 2. Study Type Classifier
# =====================================================================
def detect_study_type(text: str) -> str:
    """
    Classifies the study methodology reported in a scientific abstract excerpt.
    Differentiates Clinical Trials, Observational Studies, Animal Models, and In-Vitro experiments.
    """
    text_lower = text.lower()

    if any(k in text_lower for k in ["systematic review", "meta-analysis", "cochrane", "pooled analysis"]):
        return "Systematic Review / Meta-Analysis"
    elif any(k in text_lower for k in ["randomized", "randomised", "double-blind", "placebo-controlled", "clinical trial", "rct", "phase 3", "phase 2", "phase iii"]):
        return "Randomized Controlled Trial (Human RCT)"
    elif any(k in text_lower for k in ["cohort", "observational", "cross-sectional", "case-control", "prospective study", "survey", "retrospective"]):
        return "Observational Study (Cohort/Epidemiological)"
    elif any(k in text_lower for k in ["mice", "mouse", "murine", "rat", "rats", "animal model", "in vivo animal"]):
        return "Preclinical Animal Model (In-Vivo)"
    elif any(k in text_lower for k in ["in vitro", "cell culture", "cell line", "macrophages", "monocytes", "receptor assay", "isolated cells"]):
        return "Laboratory In-Vitro / Molecular Study"
    
    return "Biomedical Literature Abstract"


# =====================================================================
# 3. Causation vs. Correlation Detection
# =====================================================================
def check_causation_overstatement(claim: str, passage: str, study_type: str) -> bool:
    """
    Detects whether a claim uses definitive causal terminology (e.g. 'cures', 'causes',
    'proves', 'prevents') when the matched literature is observational or preclinical.
    """
    claim_lower = claim.lower()
    passage_lower = passage.lower()

    causal_terms = ["causes", "cures", "directly prevents", "guarantees", "proves", "eliminates"]
    correlational_terms = ["associated with", "correlated", "linked to", "observed in", "inverse relationship", "trend"]

    claim_has_causal = any(term in claim_lower for term in causal_terms)
    passage_has_corr = any(term in passage_lower for term in correlational_terms)

    # Flag if the claim states causation but the study is observational or in-vitro
    if claim_has_causal:
        if study_type in [
            "Observational Study (Cohort/Epidemiological)",
            "Preclinical Animal Model (In-Vivo)",
            "Laboratory In-Vitro / Molecular Study"
        ] or passage_has_corr:
            return True

    return False


# =====================================================================
# 4. Polarity & Contradiction Detection
# =====================================================================
def detect_contradiction(claim: str, passage: str) -> bool:
    """
    Detects whether a retrieved passage contradicts the claim.
    Example: Claim states 'reduces duration', but passage states 'did not reduce duration'
    or 'no significant difference'.
    """
    claim_lower = claim.lower()
    passage_lower = passage.lower()

    # Contradiction phrases indicating null or opposite findings
    negation_markers = [
        "no significant difference", "failed to show", "did not reduce",
        "no beneficial effect", "ineffective", "did not improve",
        "was not associated", "no evidence that", "failed to prevent",
        "no correlation", "evidence is absent", "trials are lacking",
        "no reliable scientific proof", "no clinical proof"
    ]

    has_negation = any(marker in passage_lower for marker in negation_markers)
    # Check if the claim asserted a positive benefit
    claim_positive = any(term in claim_lower for term in ["reduces", "improves", "benefits", "effective", "prevents", "enhances", "cure", "cures", "treats"])

    if has_negation and claim_positive:
        return True

    return False


# =====================================================================
# 5. Core Claim-Level Verification Algorithm
# =====================================================================
def verify_claim(
    claim_id: int,
    claim: str,
    chunks: List[EvidenceChunk],
    claim_embeddings: np.ndarray,
    chunk_embeddings: np.ndarray
) -> VerifiedClaim:
    """
    Verifies a single factual claim against all retrieved evidence chunks.
    Calculates semantic alignment, evaluates study design, and checks for contradictions.
    """
    if not chunks or chunk_embeddings.size == 0:
        return VerifiedClaim(
            claim_id=claim_id,
            claim_text=claim,
            status=EvidenceStatus.INSUFFICIENT_EVIDENCE,
            confidence_score=0.0,
            matched_pmid=None,
            matched_paper_title=None,
            matched_excerpt=None,
            matched_url=None,
            reason="No scientific passages were retrieved to evaluate this claim.",
            study_type="No Evidence Available",
            has_causal_overstatement=False,
            is_abstract_only=True
        )

    # 1. Extract any explicit PMID citation inside the claim (e.g. [PMID: 23775705])
    cited_pmids = re.findall(r"PMID[:\s]+(\d+)", claim, re.IGNORECASE)

    # 2. Compute Cosine Similarity between this claim and all chunk vectors
    # claim_embeddings has shape (1, D), chunk_embeddings has shape (N, D)
    similarities = np.dot(chunk_embeddings, claim_embeddings.T).flatten()
    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])
    best_chunk = chunks[best_idx]

    # If the claim explicitly cited a PMID, check if that specific paper has a strong chunk
    if cited_pmids:
        target_pmid = cited_pmids[0]
        matching_cited_indices = [i for i, c in enumerate(chunks) if c.pmid == target_pmid]
        if matching_cited_indices:
            best_cited_sub_idx = max(matching_cited_indices, key=lambda i: similarities[i])
            # If the cited paper is reasonably relevant, prioritize it for provenance transparency
            if similarities[best_cited_sub_idx] >= 0.40:
                best_idx = best_cited_sub_idx
                best_score = float(similarities[best_idx])
                best_chunk = chunks[best_idx]

    # 3. Detect study design
    study_type = detect_study_type(best_chunk.text)

    # 4. Check for causal overstatement
    causal_issue = check_causation_overstatement(claim, best_chunk.text, study_type)

    # 5. Check for direct contradiction
    is_contradicted = detect_contradiction(claim, best_chunk.text)

    # 6. Determine Classification Status
    if is_contradicted and best_score >= 0.50:
        status = EvidenceStatus.CONTRADICTED
        reason = (
            f"The retrieved peer-reviewed excerpt reports contradictory findings "
            f"(e.g., lack of effect or negative endpoint) regarding this claim."
        )

    elif best_score >= 0.65:
        if causal_issue:
            status = EvidenceStatus.PARTIALLY_SUPPORTED
            reason = (
                f"The evidence demonstrates a strong correlation ({study_type}), but the claim asserts "
                "direct clinical causation. In biomedical science, observational correlation does not equal proven causality."
            )
        elif study_type in ["Preclinical Animal Model (In-Vivo)", "Laboratory In-Vitro / Molecular Study"]:
            status = EvidenceStatus.PARTIALLY_SUPPORTED
            reason = (
                f"Directly supported at the {study_type} level. However, human clinical translation "
                "remains uncertain pending randomized clinical trials."
            )
        else:
            status = EvidenceStatus.SUPPORTED
            reason = (
                f"Directly supported by peer-reviewed literature ({study_type}) "
                f"with high semantic alignment (Cosine Similarity: {best_score:.2f})."
            )

    elif 0.45 <= best_score < 0.65:
        status = EvidenceStatus.PARTIALLY_SUPPORTED
        reason = (
            f"Passage provides moderate thematic support (Cosine Similarity: {best_score:.2f}) "
            "but lacks exhaustive clinical detail in the abstract record."
        )

    elif 0.28 <= best_score < 0.45:
        status = EvidenceStatus.UNCERTAIN_HUMAN_REVIEW
        reason = (
            f"Semantic similarity is preliminary ({best_score:.2f}). The available abstract excerpt "
            "mentions related biomedical concepts but cannot reliably verify or refute the claim without human clinical review."
        )

    else:
        status = EvidenceStatus.INSUFFICIENT_EVIDENCE
        reason = (
            f"Highest similarity score ({best_score:.2f}) is below the scientific verification cutoff. "
            "The retrieved literature does not contain adequate evidence to substantiate this claim."
        )

    return VerifiedClaim(
        claim_id=claim_id,
        claim_text=claim,
        status=status,
        confidence_score=best_score,
        matched_pmid=best_chunk.pmid,
        matched_paper_title=best_chunk.title,
        matched_excerpt=best_chunk.text,
        matched_url=best_chunk.url,
        reason=reason,
        study_type=study_type,
        has_causal_overstatement=causal_issue,
        is_abstract_only=True
    )


def verify_answer_claims(
    answer_text: str,
    chunks: List[EvidenceChunk]
) -> List[VerifiedClaim]:
    """
    Main verification pipeline:
    1. Extracts individual claims from the AI-generated answer.
    2. Encodes claims and chunks into dense vectors.
    3. Audits each claim against retrieved evidence.
    4. Returns a comprehensive list of VerifiedClaim objects.
    """
    if not answer_text or not chunks:
        return []

    claims = extract_claims_from_answer(answer_text)
    if not claims:
        logger.info("No distinct factual claims extracted for verification.")
        return []

    logger.info(f"Auditing {len(claims)} factual claims against {len(chunks)} evidence chunks...")

    # Encode all claims in a single batch
    claim_vectors = generate_embeddings(claims)

    # Encode all chunks in a single batch
    chunk_texts = [c.text for c in chunks]
    chunk_vectors = generate_embeddings(chunk_texts)

    verified_claims: List[VerifiedClaim] = []
    for idx, claim in enumerate(claims, 1):
        claim_vec = claim_vectors[idx - 1 : idx]
        verified_item = verify_claim(
            claim_id=idx,
            claim=claim,
            chunks=chunks,
            claim_embeddings=claim_vec,
            chunk_embeddings=chunk_vectors
        )
        verified_claims.append(verified_item)

    return verified_claims


def evaluate_abstention_triggers(
    search_query: str,
    papers: List[PaperMetadata],
    chunks: List[EvidenceChunk],
    top_similarity_score: float,
    threshold: float = config.MIN_SIMILARITY_THRESHOLD,
    verified_claims: Optional[List[VerifiedClaim]] = None
) -> Optional[AbstentionReport]:
    """
    Evaluates whether the system must abstain from providing a confident answer.
    Triggers when:
    1. No relevant papers are retrieved.
    2. Retrieved abstracts do not contain enough usable text.
    3. The evidence does not address the question (top similarity < threshold).
    4. Evidence is conflicting (contradictions detected across retrieved studies).
    5. Claims cannot be linked to reliable supporting passages.
    
    Returns:
        AbstentionReport if an abstention is triggered; None if evidence is sufficient.
    """
    # 1. No relevant papers retrieved
    if not papers:
        return AbstentionReport(
            is_abstained=True,
            search_query=search_query,
            papers_retrieved_count=0,
            reason="No peer-reviewed publications matching this query could be located in the NCBI PubMed database.",
            additional_research_required="Broaden the search terms to include alternative disease synonyms, related drug classes, or general biological pathways."
        )

    # 2. Retrieved abstracts do not contain enough information
    if not chunks:
        return AbstentionReport(
            is_abstained=True,
            search_query=search_query,
            papers_retrieved_count=len(papers),
            reason="Retrieved PubMed publications are title-only citations or lack structured abstract text.",
            additional_research_required="Access full-text publications via open-access institutional repositories or publisher databases."
        )

    # 3. Evidence does not address the question (top similarity < threshold)
    if top_similarity_score < threshold:
        return AbstentionReport(
            is_abstained=True,
            search_query=search_query,
            papers_retrieved_count=len(papers),
            reason=f"The closest retrieved scientific passage had a cosine similarity score of {top_similarity_score:.2f}, which is below our strict confidence threshold ({threshold:.2f}). The literature does not directly address the clinical question.",
            additional_research_required="Targeted interventional trials or clinical studies specifically investigating this exact biomedical hypothesis."
        )

    # 4. Evidence explicitly documents absence of clinical proof or human trials
    combined_passage_text = " ".join([c.text.lower() for c in chunks])
    absence_markers = [
        "evidence is absent", "trials are lacking", "no reliable scientific proof",
        "no evidence of efficacy", "clinical evidence is lacking", "lack of clinical evidence",
        "no clinical trials", "no proof of efficacy", "therapeutic claims cannot be made",
        "no clinical therapeutic claims can be made"
    ]
    query_lower = search_query.lower()
    if any(m in combined_passage_text for m in absence_markers):
        if any(term in query_lower for term in ["cure", "cures", "treat", "effective", "prevent", "reversing"]):
            return AbstentionReport(
                is_abstained=True,
                search_query=search_query,
                papers_retrieved_count=len(papers),
                reason="Retrieved scientific literature explicitly documents an absence of human clinical trials and notes that therapeutic claims are not substantiated by trial data.",
                additional_research_required="Phase II and Phase III randomized placebo-controlled clinical trials in human cohorts to establish efficacy."
            )

    # 5. Check for conflicting evidence or unsupported claims if verified claims were provided
    if verified_claims:
        contradicted_claims = [c for c in verified_claims if c.status == EvidenceStatus.CONTRADICTED]
        supported_claims = [c for c in verified_claims if c.status in (EvidenceStatus.SUPPORTED, EvidenceStatus.PARTIALLY_SUPPORTED)]
        
        # If the evidence is predominantly conflicting
        if len(contradicted_claims) > 0 and len(supported_claims) == 0:
            return AbstentionReport(
                is_abstained=True,
                search_query=search_query,
                papers_retrieved_count=len(papers),
                reason="Available peer-reviewed literature presents conflicting or null-effect findings that directly contradict the premise of the inquiry.",
                additional_research_required="A systematic review and meta-analysis pooling high-powered randomized controlled trials to resolve conflicting outcomes."
            )

        # 5. Claims cannot be linked to reliable supporting passages
        if len(supported_claims) == 0:
            return AbstentionReport(
                is_abstained=True,
                search_query=search_query,
                papers_retrieved_count=len(papers),
                reason="Factual assertions regarding this inquiry could not be linked to reliable, verified supporting passages in the retrieved abstracts.",
                additional_research_required="Peer-reviewed randomized controlled trials with standardized endpoint measurements."
            )

    return None


# =====================================================================
# Backward Compatibility: Document-Level Sufficiency Function
# =====================================================================
def evaluate_evidence_sufficiency(
    chunks: List[EvidenceChunk],
    threshold: float = config.MIN_SIMILARITY_THRESHOLD
) -> Tuple[bool, str, str, float, List[EvidenceChunk]]:
    """
    Maintains compatibility with RAG pipeline's document-level abstention check.
    """
    if not chunks:
        return (
            False,
            "Insufficient",
            "No scientific literature matching this query could be found in PubMed.",
            0.0,
            []
        )

    scores = [c.score for c in chunks if c.score is not None]
    top_score = max(scores) if scores else 0.0

    qualifying = [c for c in chunks if c.score is not None and c.score >= threshold]

    if top_score < threshold or not qualifying:
        reason = (
            f"The highest similarity score ({top_score:.2f}) fell below our strict "
            f"scientific confidence threshold ({threshold:.2f}). "
            "To prevent biomedical hallucinations, EvidenceBot abstains from answering."
        )
        return (False, "Insufficient", reason, top_score, [])

    if top_score >= 0.60 and len(qualifying) >= 3:
        confidence = "High"
    elif top_score >= 0.45:
        confidence = "Moderate"
    else:
        confidence = "Preliminary"

    reason = f"Located {len(qualifying)} relevant evidence passage(s) with maximum similarity of {top_score:.2f}."
    return (True, confidence, reason, top_score, qualifying)

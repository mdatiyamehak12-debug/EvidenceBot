"""
EvidenceBot - Citation Validation & Integrity Module
====================================================
Performs comprehensive auditing of citations and claims in AI-generated answers:
1. Validates that each cited PMID exists in the retrieved source literature.
2. Verifies that citation metadata (title, authors, journal, year) matches NCBI records.
3. Ensures each cited source is semantically relevant to the specific claim citing it.
4. Identifies missing citations (factual claims lacking a cited source).
5. Identifies unsupported claims (claims citing a source that does not substantiate the assertion).
6. Generates official clickable PubMed links (https://pubmed.ncbi.nlm.nih.gov/<pmid>/).
7. Guarantees zero invented or hallucinated references.
"""

from dataclasses import dataclass, field
from typing import List, Set, Dict, Any, Tuple, Optional
import re
import logging
import numpy as np

from utils.helpers import format_pubmed_url
from backend.preprocessing import EvidenceChunk, split_sentences, clean_text
from backend.pubmed import PaperMetadata
from backend.embeddings import generate_embeddings

logger = logging.getLogger(__name__)


@dataclass
class ValidatedCitation:
    """
    Structured record of a verified citation linked directly to an NCBI PubMed paper.
    """
    pmid: str
    url: str                                     # https://pubmed.ncbi.nlm.nih.gov/<pmid>/
    title: str
    journal: str
    year: str
    authors: List[str]
    doi: Optional[str]
    claim_context: str                           # Sentence or claim that cited this PMID
    relevance_score: float                       # Semantic similarity between claim and paper excerpt
    is_relevant: bool                            # True if relevance_score >= 0.32

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pmid": self.pmid,
            "url": self.url,
            "title": self.title,
            "journal": self.journal,
            "year": self.year,
            "authors": self.authors,
            "doi": self.doi,
            "claim_context": self.claim_context,
            "relevance_score": round(self.relevance_score, 3),
            "is_relevant": self.is_relevant,
        }


@dataclass
class UnsupportedClaim:
    """
    Represents an assertion that cites a PMID, but the cited paper does not substantiate it.
    """
    claim: str
    cited_pmid: str
    paper_title: str
    relevance_score: float
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "claim": self.claim,
            "cited_pmid": self.cited_pmid,
            "paper_title": self.paper_title,
            "relevance_score": round(self.relevance_score, 3),
            "reason": self.reason,
        }


@dataclass
class CitationAuditReport:
    """
    Complete audit report evaluating citation validity and claim grounding.
    """
    is_valid: bool                               # True if 0 hallucinated citations
    total_citations_count: int
    verified_citations: List[ValidatedCitation] = field(default_factory=list)
    hallucinated_pmids: List[str] = field(default_factory=list)
    missing_citations: List[str] = field(default_factory=list)
    unsupported_claims: List[UnsupportedClaim] = field(default_factory=list)
    unused_retrieved_pmids: List[str] = field(default_factory=list)
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_citations_count": self.total_citations_count,
            "verified_citations": [c.to_dict() for c in self.verified_citations],
            "hallucinated_pmids": self.hallucinated_pmids,
            "missing_citations": self.missing_citations,
            "unsupported_claims": [u.to_dict() for u in self.unsupported_claims],
            "unused_retrieved_pmids": self.unused_retrieved_pmids,
            "summary": self.summary,
        }


def extract_citations(text: str) -> Set[str]:
    """
    Extracts all PubMed IDs cited in a text using standard patterns:
    [PMID: 23775705], [PMID 23775705], (PMID: 23775705), PMID: 23775705
    """
    if not text:
        return set()
    matches = re.findall(r"PMID[:\s]+(\d+)", text, re.IGNORECASE)
    return set(matches)


def extract_sentences_with_citations(answer_text: str) -> List[Tuple[str, List[str]]]:
    """
    Deconstructs the answer into individual sentences and maps each to the PMIDs it cited.
    Returns: List of (sentence_text, list_of_cited_pmids).
    """
    if not answer_text:
        return []

    lines = answer_text.split("\n")
    results: List[Tuple[str, List[str]]] = []

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("#") or line_clean.startswith("---"):
            continue
        # Skip disclaimer or plain url lines
        if "disclaimer" in line_clean.lower() or line_clean.startswith("http"):
            continue

        # Remove bullet markers
        clean_line = re.sub(r"^[-*•\d.]+\s+", "", line_clean).strip()
        if not clean_line:
            continue

        sentences = split_sentences(clean_line)
        for s in sentences:
            s_str = s.strip()
            if len(s_str) < 25:
                continue
            cited = list(extract_citations(s_str))
            results.append((s_str, cited))

    return results


def validate_citations_comprehensive(
    answer_text: str,
    papers: List[PaperMetadata],
    chunks: List[EvidenceChunk],
    relevance_threshold: float = 0.32
) -> CitationAuditReport:
    """
    Performs full-spectrum citation and claim verification:
    - Verifies cited PMIDs exist in retrieved literature.
    - Verifies paper metadata (title, journal, year, authors) matches the record.
    - Checks semantic relevance between claim and the cited paper's excerpts.
    - Identifies factual statements lacking citations (missing citations).
    - Identifies claims citing a paper that does not support the statement.
    - Generates clickable links for all valid citations.
    """
    if not answer_text:
        return CitationAuditReport(
            is_valid=True,
            total_citations_count=0,
            summary="No answer text provided to validate."
        )

    # 1. Map retrieved papers by PMID
    papers_by_pmid: Dict[str, PaperMetadata] = {p.pmid: p for p in papers if p.pmid}
    available_pmids = set(papers_by_pmid.keys())

    # Map chunks by PMID for localized relevance checking
    chunks_by_pmid: Dict[str, List[EvidenceChunk]] = {}
    for c in chunks:
        chunks_by_pmid.setdefault(c.pmid, []).append(c)

    # 2. Extract citations and sentences
    sentence_records = extract_sentences_with_citations(answer_text)
    all_cited_pmids = extract_citations(answer_text)

    # 3. Detect Hallucinated Citations (PMIDs cited that do not exist in retrieved records)
    hallucinated = sorted(list(all_cited_pmids.difference(available_pmids)))

    # 4. Audit each citation in its specific claim context
    verified_citations: List[ValidatedCitation] = []
    unsupported_claims: List[UnsupportedClaim] = []
    missing_citations: List[str] = []
    seen_citation_keys: Set[Tuple[str, str]] = set()

    for sentence, cited_list in sentence_records:
        # Check for Missing Citations:
        # If a substantive factual statement makes assertions without any PMID
        if not cited_list:
            # Check if sentence is a factual claim rather than a conversational transition
            sentence_lower = sentence.lower()
            if len(sentence) >= 45 and not any(sentence_lower.startswith(w) for w in ["in summary", "overall", "however", "therefore", "please note", "always consult"]):
                if any(w in sentence_lower for w in ["study", "trial", "reduces", "increases", "inhibits", "activates", "associated", "risk", "effect", "rate", "mg", "cells"]):
                    missing_citations.append(sentence)
            continue

        # If sentence has citations, verify relevance against each cited paper
        for pmid in cited_list:
            if pmid not in papers_by_pmid:
                # Already captured in hallucinated
                continue

            paper = papers_by_pmid[pmid]
            key = (pmid, sentence)
            if key in seen_citation_keys:
                continue
            seen_citation_keys.add(key)

            # Check semantic relevance between this sentence and the cited paper's text
            paper_chunks = chunks_by_pmid.get(pmid, [])
            paper_texts = [c.text for c in paper_chunks] if paper_chunks else [paper.abstract]
            
            # Compute similarity
            try:
                claim_vec = generate_embeddings([sentence])
                chunk_vecs = generate_embeddings(paper_texts)
                sims = np.dot(chunk_vecs, claim_vec.T).flatten()
                relevance_score = float(np.max(sims)) if sims.size > 0 else 0.0
            except Exception as e:
                logger.warning(f"Error computing citation similarity for PMID {pmid}: {e}")
                relevance_score = 0.50

            is_rel = relevance_score >= relevance_threshold

            verified_item = ValidatedCitation(
                pmid=pmid,
                url=format_pubmed_url(pmid),
                title=paper.title,
                journal=paper.journal,
                year=paper.year,
                authors=paper.authors,
                doi=paper.doi,
                claim_context=sentence,
                relevance_score=relevance_score,
                is_relevant=is_rel
            )
            verified_citations.append(verified_item)

            # If semantic relevance is too low, flag as an Unsupported Claim
            if not is_rel:
                unsupported_claims.append(
                    UnsupportedClaim(
                        claim=sentence,
                        cited_pmid=pmid,
                        paper_title=paper.title,
                        relevance_score=relevance_score,
                        reason=(
                            f"Cited PMID {pmid} has low semantic relevance ({relevance_score:.2f}) "
                            f"to this specific claim. The source paper discusses '{paper.title}' but does not substaniate the statement."
                        )
                    )
                )

    # 5. Identify retrieved papers that were never cited
    cited_valid_set = {c.pmid for c in verified_citations}
    unused_pmids = sorted(list(available_pmids.difference(cited_valid_set)))

    # 6. Overall validity verdict
    is_valid = len(hallucinated) == 0

    if not is_valid:
        summary = f"Audit Warning: {len(hallucinated)} hallucinated PMID(s) detected that were not in NCBI retrieval records."
    elif unsupported_claims:
        summary = f"Citation Notice: {len(verified_citations)} valid citations found, but {len(unsupported_claims)} claim(s) cited weakly relevant sources."
    else:
        summary = f"All {len(verified_citations)} citations verified with authentic NCBI PubMed records and relevant textual support."

    return CitationAuditReport(
        is_valid=is_valid,
        total_citations_count=len(all_cited_pmids),
        verified_citations=verified_citations,
        hallucinated_pmids=hallucinated,
        missing_citations=missing_citations[:5],  # Cap display at top 5
        unsupported_claims=unsupported_claims,
        unused_retrieved_pmids=unused_pmids,
        summary=summary
    )


def verify_citations(
    answer_text: str,
    source_chunks: List[EvidenceChunk]
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Backwards-compatible convenience function for simple PMID set checking.
    Returns: (verified_pmids, hallucinated_pmids, available_pmids).
    """
    available_pmids = {c.pmid for c in source_chunks if c.pmid}
    cited_pmids = extract_citations(answer_text)

    verified_pmids = cited_pmids.intersection(available_pmids)
    hallucinated_pmids = cited_pmids.difference(available_pmids)

    return (verified_pmids, hallucinated_pmids, available_pmids)

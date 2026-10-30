"""
EvidenceBot - Abstract Preprocessing & Chunking Module
======================================================
Cleans biomedical text and splits multi-sentence abstracts into manageable,
context-rich chunks while strictly preserving PMID and source provenance.

Requirements handled:
- Preserves PMID, title, journal, year, and URL for every chunk.
- Filters out papers without genuine abstracts (does not embed empty abstracts).
- Deduplicates incoming papers by PMID.
- Splits text cleanly while protecting biomedical abbreviations.
"""

from dataclasses import dataclass
from typing import List, Optional, Set
import re
import logging

from utils import config
from backend.pubmed import PaperMetadata, NO_ABSTRACT_TEXT

logger = logging.getLogger(__name__)


@dataclass
class EvidenceChunk:
    """
    Represents an atomic segment of scientific evidence from a peer-reviewed abstract.
    Every chunk retains full provenance back to the original PubMed record.
    """
    chunk_id: str                              # Unique identifier, e.g. "34322844_chunk_0"
    pmid: str                                  # Official PubMed ID
    title: str                                 # Article title
    text: str                                  # The chunk text (2-4 sentences)
    url: str = ""                              # https://pubmed.ncbi.nlm.nih.gov/<pmid>/
    journal: str = "Unknown Journal"           # Journal name
    year: str = "Unknown Year"                 # Publication year
    score: Optional[float] = None              # Cosine similarity score (populated by vector search)

    def __post_init__(self):
        if not self.url and self.pmid:
            from utils.helpers import format_pubmed_url
            self.url = format_pubmed_url(self.pmid)

    def to_citation_header(self) -> str:
        """Human-readable citation header for LLM prompts or UI display."""
        return f"[PMID: {self.pmid}] ({self.title}, {self.journal} {self.year})"

    def to_context_snippet(self) -> str:
        """Formatted snippet specifically designed for feeding into LLM RAG prompts."""
        return f"Source: [PMID: {self.pmid}] ({self.title})\nExcerpt: \"{self.text}\""


def clean_text(text: str) -> str:
    """
    Normalizes whitespace and removes anomalous characters or XML residues from abstracts.
    Example: 'Cells   were \n incubated.\t' -> 'Cells were incubated.'
    """
    if not text:
        return ""
    # Collapse multiple whitespaces, tabs, and newlines into a single space
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def split_sentences(text: str) -> List[str]:
    """
    Splits text into individual sentences while protecting common medical and research
    abbreviations (e.g., 'et al.', 'Dr.', 'vs.', 'p < 0.05', 'i.e.', 'e.g.').
    """
    if not text:
        return []

    # Map of abbreviations to temporary tokens so the regex doesn't split on them
    abbreviation_tokens = {
        "et al.": "et al_TOKEN_",
        "e.g.": "e_TOKEN_g_TOKEN_",
        "i.e.": "i_TOKEN_e_TOKEN_",
        "vs.": "vs_TOKEN_",
        "Dr.": "Dr_TOKEN_",
        "Prof.": "Prof_TOKEN_",
        "Fig.": "Fig_TOKEN_",
        "approx.": "approx_TOKEN_",
        "p <": "p_LT_",
        "p >": "p_GT_",
        "p =": "p_EQ_",
    }

    protected_text = text
    for abbr, token in abbreviation_tokens.items():
        protected_text = protected_text.replace(abbr, token)

    # Split on sentence boundaries:
    # A period, exclamation, or question mark followed by whitespace and a capital letter or digit
    raw_sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z0-9])', protected_text)

    # Restore the original tokens and clean up each sentence
    clean_sentences: List[str] = []
    for s in raw_sentences:
        restored = s
        for abbr, token in abbreviation_tokens.items():
            restored = restored.replace(token, abbr)
        final_s = restored.strip()
        if final_s:
            clean_sentences.append(final_s)

    return clean_sentences if clean_sentences else [text.strip()]


def chunk_papers(
    papers: List[PaperMetadata],
    chunk_size: int = config.CHUNK_SIZE_SENTENCES,
    overlap: int = config.CHUNK_OVERLAP_SENTENCES
) -> List[EvidenceChunk]:
    """
    Converts a collection of PaperMetadata records into EvidenceChunk objects.
    
    Guarantees:
    1. Deduplication: Ensures no PMID is processed more than once.
    2. Abstract Filtering: Ignores papers with missing or empty abstracts.
    3. Metadata Provenance: Every single chunk stores the exact PMID, title, journal, year, and URL.
    4. Overlapping Window: Consecutive chunks overlap by 1 sentence so contextual meaning is not cut off.
    
    Parameters:
        papers: List of retrieved PubMed papers.
        chunk_size: Number of sentences grouped into each chunk (default: 3).
        overlap: Number of sentences overlapping between consecutive chunks (default: 1).
        
    Returns:
        List[EvidenceChunk]: List of processed evidence chunks ready for embedding.
    """
    all_chunks: List[EvidenceChunk] = []
    seen_pmids: Set[str] = set()

    for paper in papers:
        # 1. Skip duplicate papers
        if paper.pmid in seen_pmids:
            continue
        seen_pmids.add(paper.pmid)

        # 2. Skip empty abstracts (do NOT embed papers without genuine abstract text)
        if not paper.has_abstract or not paper.abstract:
            logger.info(f"Skipping PMID {paper.pmid} from chunking: No abstract text available.")
            continue
        if paper.abstract.strip() == NO_ABSTRACT_TEXT:
            continue

        # 3. Clean and split abstract into sentences
        cleaned_abstract = clean_text(paper.abstract)
        sentences = split_sentences(cleaned_abstract)

        if not sentences:
            continue

        # 4. Slide a window across sentences to build overlapping chunks
        step = max(1, chunk_size - overlap)
        chunk_idx = 0

        for i in range(0, len(sentences), step):
            window = sentences[i : i + chunk_size]
            if not window:
                continue
            
            chunk_content = " ".join(window).strip()
            
            # Avoid creating tiny residual chunks with less than 25 characters
            if len(chunk_content) < 25 and all_chunks:
                continue

            chunk = EvidenceChunk(
                chunk_id=f"{paper.pmid}_chunk_{chunk_idx}",
                pmid=paper.pmid,
                title=paper.title,
                journal=paper.journal,
                year=paper.year,
                text=chunk_content,
                url=paper.url,
            )
            all_chunks.append(chunk)
            chunk_idx += 1

    return all_chunks

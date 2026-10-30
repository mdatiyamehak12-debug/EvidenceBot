"""
EvidenceBot - Helper Functions
==============================
Contains small, reusable utility functions used across the app
such as text cleaning, URL formatting, and display helpers.
"""

from typing import List
from utils import config


def format_pubmed_url(pmid: str) -> str:
    """
    Constructs a verified direct link to a paper on the official PubMed website.
    Example: '23775705' -> 'https://pubmed.ncbi.nlm.nih.gov/23775705/'
    """
    clean_pmid = str(pmid).strip()
    return f"{config.PUBMED_BASE_URL}{clean_pmid}/"


def truncate_text(text: str, max_chars: int = 150) -> str:
    """
    Truncates a long string to a given length and appends an ellipsis (...)
    useful for displaying clean paper previews in the user interface.
    """
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def format_author_list(authors: List[str], max_to_display: int = 3) -> str:
    """
    Formats a list of author names cleanly (e.g., 'Smith J, Doe A, et al.').
    """
    if not authors:
        return "Authors not listed"
    if len(authors) <= max_to_display:
        return ", ".join(authors)
    return ", ".join(authors[:max_to_display]) + " et al."


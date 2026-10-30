"""
EvidenceBot - PubMed Research Paper Retrieval Module
=====================================================
Interacts with the official NCBI (National Center for Biotechnology Information)
Entrez E-utilities API to retrieve authentic, peer-reviewed biomedical literature.

Official NCBI Documentation:
https://www.ncbi.nlm.nih.gov/books/NBK25501/

Components Used:
- ESearch: Searches PubMed index and returns matching PubMed Identifiers (PMIDs).
- EFetch: Downloads structured XML records for given PMIDs (titles, authors, abstracts, etc.).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import xml.etree.ElementTree as ET
import time
import re
import logging
import requests

from utils import config
from utils.helpers import format_pubmed_url

logger = logging.getLogger(__name__)

# Standard fallback message when PubMed has no abstract indexed
NO_ABSTRACT_TEXT = "No abstract available in the official PubMed record."


def build_pubmed_query(query: str) -> str:
    """
    Transforms a natural language biomedical question into an optimized PubMed search string.
    PubMed ESearch uses Boolean keyword matching. Natural conversational words
    (e.g., 'What is the role of', '?') often cause zero matches.
    
    This function removes conversational filler words while preserving key biomedical terminology
    and essential single-letter tokens (e.g. 'vitamin D', 'T cell', 'B cell').
    """
    if not query:
        return ""

    # Remove punctuation characters (like '?' or '!') except hyphens within words
    cleaned = re.sub(r'[^\w\s-]', ' ', query)

    # Conversational stop words that restrict PubMed keyword search
    stop_words = {
        'what', 'is', 'the', 'role', 'of', 'in', 'how', 'does', 'can', 'why',
        'are', 'which', 'do', 'a', 'an', 'and', 'or', 'for', 'to', 'on', 'with', 'about', 'explain'
    }

    tokens = [w for w in cleaned.split() if w.lower() not in stop_words]
    if not tokens:
        return cleaned.strip()
    return " ".join(tokens)


@dataclass
class PaperMetadata:
    """
    Structured representation of a peer-reviewed article from PubMed.
    Every field guarantees complete provenance back to NCBI.
    """
    pmid: str                          # Official PubMed ID (e.g., '21527855')
    title: str                         # Article title
    abstract: str                      # Abstract text or notice of absence
    has_abstract: bool = True          # Distinguishes genuine abstract from missing abstract
    journal: str = "Unknown Journal"   # Academic journal name
    year: str = "Unknown Year"         # Publication year
    authors: List[str] = field(default_factory=list)  # Author list
    doi: Optional[str] = None          # Digital Object Identifier
    url: str = ""                      # Official web link: https://pubmed.ncbi.nlm.nih.gov/<pmid>/

    def __post_init__(self):
        # Ensure the verified PubMed URL is always generated
        if not self.url and self.pmid:
            self.url = format_pubmed_url(self.pmid)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the object to a dictionary for UI or JSON export."""
        return {
            "pmid": self.pmid,
            "title": self.title,
            "abstract": self.abstract,
            "has_abstract": self.has_abstract,
            "journal": self.journal,
            "year": self.year,
            "authors": self.authors,
            "doi": self.doi,
            "url": self.url,
        }


@dataclass
class SearchResult:
    """
    Detailed payload returned by a PubMed retrieval operation.
    Enables the UI to cleanly distinguish between empty search results,
    missing abstracts, and network errors.
    """
    query: str
    total_found: int
    pmids: List[str] = field(default_factory=list)
    papers: List[PaperMetadata] = field(default_factory=list)
    is_empty: bool = False
    error_message: Optional[str] = None


class PubMedRetriever:
    """
    Client for the NCBI Entrez E-Utilities API.
    Adheres strictly to NCBI usage guidelines, rate limiting, and headers.
    """

    def __init__(self, email: Optional[str] = None, api_key: Optional[str] = None):
        # NCBI requires tool name and email to avoid automated IP-blocking
        self.email = email or config.NCBI_EMAIL
        self.api_key = api_key or config.NCBI_API_KEY
        self.tool = config.NCBI_TOOL_NAME
        
        # Enforce rate limit delay:
        # Without API key: max 3 requests/sec (0.35s delay)
        # With API key: max 10 requests/sec (0.11s delay)
        self.rate_delay = 0.12 if self.api_key else 0.36
        self._last_request_time = 0.0

    def _apply_rate_limit(self):
        """Enforces compliant request intervals to respect NCBI servers."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_delay:
            time.sleep(self.rate_delay - elapsed)
        self._last_request_time = time.time()

    def _get_base_params(self) -> Dict[str, str]:
        """Prepares standard NCBI parameter dictionary."""
        params = {
            "tool": self.tool,
            "email": self.email,
        }
        if self.api_key:
            params["api_key"] = self.api_key
        return params

    def _execute_esearch(self, term: str, max_results: int) -> List[str]:
        """Helper to run a single ESearch request with retry logic."""
        self._apply_rate_limit()

        params = self._get_base_params()
        params.update({
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "retmax": str(min(max_results, config.MAX_CANDIDATE_PAPERS)),
            "sort": "relevance",
        })

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    config.NCBI_ESEARCH_URL,
                    params=params,
                    timeout=15
                )

                # Rate limit handling (HTTP 429)
                if response.status_code == 429:
                    wait_time = (attempt + 1) * 2.0
                    logger.warning(f"NCBI rate limit reached (HTTP 429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()
                raw_pmids = data.get("esearchresult", {}).get("idlist", [])
                return list(dict.fromkeys(raw_pmids))

            except requests.Timeout:
                logger.warning(f"NCBI ESearch timeout on attempt {attempt + 1}/{max_retries}.")
                if attempt == max_retries - 1:
                    return []
                time.sleep(1.0)
            except requests.RequestException as req_err:
                logger.error(f"Error executing PubMed ESearch for '{term}': {req_err}")
                return []

        return []

    def search(self, query: str, max_results: int = config.DEFAULT_MAX_PAPERS) -> List[str]:
        """
        Executes an ESearch query on PubMed to obtain relevant PMIDs.
        Uses query optimization for natural language questions.
        
        Parameters:
            query (str): Clinical question or search term.
            max_results (int): Maximum number of PMIDs to return.
            
        Returns:
            List[str]: Deduplicated list of matching PubMed IDs.
        """
        clean_query = query.strip()
        if not clean_query:
            return []

        # 1. First attempt with cleaned keywords
        optimized_query = build_pubmed_query(clean_query)
        pmids = self._execute_esearch(optimized_query, max_results)

        # 2. Fallback to raw query if keyword optimization produced 0 results
        if not pmids and optimized_query != clean_query:
            pmids = self._execute_esearch(clean_query, max_results)

        return pmids

    def fetch_details(self, pmids: List[str]) -> List[PaperMetadata]:
        """
        Retrieves full XML records for a list of PMIDs via EFetch and extracts metadata.
        
        Parameters:
            pmids (List[str]): List of PubMed IDs to fetch.
            
        Returns:
            List[PaperMetadata]: Parsed scientific paper objects.
        """
        if not pmids:
            return []

        unique_pmids = list(dict.fromkeys(pmids))
        self._apply_rate_limit()

        params = self._get_base_params()
        params.update({
            "db": "pubmed",
            "id": ",".join(unique_pmids),
            "retmode": "xml",
        })

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    config.NCBI_EFETCH_URL,
                    params=params,
                    timeout=25
                )

                if response.status_code == 429:
                    wait_time = (attempt + 1) * 2.0
                    logger.warning(f"NCBI EFetch rate limit (HTTP 429). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                return self.parse_xml(response.content)

            except requests.Timeout:
                logger.warning(f"NCBI EFetch timeout on attempt {attempt + 1}/{max_retries}.")
                if attempt == max_retries - 1:
                    return []
                time.sleep(1.0)
            except requests.RequestException as req_err:
                logger.error(f"Error executing PubMed EFetch: {req_err}")
                return []

        return []

    def parse_xml(self, xml_bytes: bytes) -> List[PaperMetadata]:
        """
        Parses NCBI PubmedArticleSet XML into structured PaperMetadata records.
        Uses standard library xml.etree.ElementTree for speed and portability.
        """
        papers: List[PaperMetadata] = []
        try:
            root = ET.fromstring(xml_bytes)
        except ET.ParseError as err:
            logger.error(f"Failed to parse PubMed XML data: {err}")
            return papers

        for article_elem in root.findall(".//PubmedArticle"):
            try:
                # 1. Extract PMID (Mandatory)
                pmid_node = article_elem.find(".//MedlineCitation/PMID")
                if pmid_node is None or not pmid_node.text:
                    continue
                pmid = pmid_node.text.strip()

                # 2. Extract Title
                title_node = article_elem.find(".//ArticleTitle")
                title = "".join(title_node.itertext()).strip() if title_node is not None else "Untitled Scientific Publication"
                if title.endswith("."):
                    title = title[:-1].strip()

                # 3. Extract Abstract (Supports structured sections: BACKGROUND, METHODS, RESULTS, etc.)
                abstract_sections: List[str] = []
                for text_elem in article_elem.findall(".//Abstract/AbstractText"):
                    label = text_elem.attrib.get("Label") or text_elem.attrib.get("NlmCategory")
                    text_content = "".join(text_elem.itertext()).strip()
                    if text_content:
                        if label:
                            abstract_sections.append(f"{label.capitalize()}: {text_content}")
                        else:
                            abstract_sections.append(text_content)

                if abstract_sections:
                    abstract = "\n\n".join(abstract_sections).strip()
                    has_abstract = True
                else:
                    abstract = NO_ABSTRACT_TEXT
                    has_abstract = False

                # 4. Extract Academic Journal
                journal_node = article_elem.find(".//Journal/Title")
                if journal_node is None or not journal_node.text:
                    journal_node = article_elem.find(".//MedlineJournalInfo/MedlineTA")
                journal = journal_node.text.strip() if journal_node is not None and journal_node.text else "Biomedical Journal"

                # 5. Extract Publication Year
                year = "Unknown"
                year_node = article_elem.find(".//JournalIssue/PubDate/Year")
                if year_node is not None and year_node.text:
                    year = year_node.text.strip()
                else:
                    medline_date = article_elem.find(".//JournalIssue/PubDate/MedlineDate")
                    if medline_date is not None and medline_date.text:
                        m = re.search(r"\b(19\d\d|20\d\d)\b", medline_date.text)
                        if m:
                            year = m.group(1)

                # 6. Extract Authors
                authors: List[str] = []
                for author_elem in article_elem.findall(".//AuthorList/Author")[:6]:
                    last = author_elem.find("LastName")
                    fore = author_elem.find("ForeName")
                    if fore is None:
                        fore = author_elem.find("Initials")

                    last_str = last.text.strip() if last is not None and last.text else ""
                    fore_str = fore.text.strip() if fore is not None and fore.text else ""

                    if last_str and fore_str:
                        authors.append(f"{fore_str} {last_str}")
                    elif last_str:
                        authors.append(last_str)
                    elif author_elem.find("CollectiveName") is not None:
                        col_elem = author_elem.find("CollectiveName")
                        if col_elem.text:
                            authors.append(col_elem.text.strip())

                # 7. Extract DOI (Digital Object Identifier)
                doi = None
                for article_id in article_elem.findall(".//ArticleIdList/ArticleId"):
                    if article_id.attrib.get("IdType") == "doi" and article_id.text:
                        doi = article_id.text.strip()
                        break
                if not doi:
                    for eloc in article_elem.findall(".//ELocationID"):
                        if eloc.attrib.get("EIdType") == "doi" and eloc.text:
                            doi = eloc.text.strip()
                            break

                paper = PaperMetadata(
                    pmid=pmid,
                    title=title,
                    abstract=abstract,
                    has_abstract=has_abstract,
                    journal=journal,
                    year=year,
                    authors=authors,
                    doi=doi,
                )
                papers.append(paper)

            except Exception as item_err:
                logger.warning(f"Error parsing PubMed article entry: {item_err}")
                continue

        return papers

    def retrieve(self, query: str, max_results: int = config.DEFAULT_MAX_PAPERS) -> SearchResult:
        """
        Unified method: Searches PubMed and fetches structured metadata for all matches.
        Returns a SearchResult object distinguishing empty search from missing abstracts.
        """
        pmids = self.search(query, max_results=max_results)
        
        if not pmids:
            return SearchResult(
                query=query,
                total_found=0,
                pmids=[],
                papers=[],
                is_empty=True,
                error_message=None
            )

        papers = self.fetch_details(pmids)
        
        return SearchResult(
            query=query,
            total_found=len(pmids),
            pmids=pmids,
            papers=papers,
            is_empty=False,
            error_message=None
        )


# =====================================================================
# Functional Interface (Backwards-Compatible with existing code)
# =====================================================================
_default_retriever = PubMedRetriever()


def search_pubmed(query: str, max_results: int = config.DEFAULT_MAX_PAPERS) -> List[str]:
    """Convenience function to search PubMed for PMIDs."""
    return _default_retriever.search(query, max_results=max_results)


def fetch_paper_details(pmids: List[str]) -> List[PaperMetadata]:
    """Convenience function to fetch parsed PaperMetadata for PMIDs."""
    return _default_retriever.fetch_details(pmids)


def parse_pubmed_xml(xml_bytes: bytes) -> List[PaperMetadata]:
    """Convenience function to parse PubMed XML data."""
    return _default_retriever.parse_xml(xml_bytes)

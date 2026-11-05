"""
EvidenceBot - Configuration Module
===================================
Centralizes all application settings, API endpoints, model choices,
and threshold values in one place so you never have to hardcode settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# 1. Base Paths & Environment Variables
# -------------------------------------------------------------------------
# Automatically locates the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent

# Load configuration and secrets from the .env file in the project root
load_dotenv(ROOT_DIR / ".env")

# -------------------------------------------------------------------------
# 2. PubMed NCBI API Settings
# -------------------------------------------------------------------------
# NCBI asks automated tools to send an email to identify the application
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "evidencebot_user@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")

# Official NCBI E-Utilities web endpoints
NCBI_ESEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
NCBI_TOOL_NAME = "EvidenceBot_Biomedical_Assistant"

# Standard PubMed web link format for citing papers
PUBMED_BASE_URL = "https://pubmed.ncbi.nlm.nih.gov/"

# Maximum number of papers to fetch per search (supports manual limit up to 100)
DEFAULT_MAX_PAPERS = 10
MAX_CANDIDATE_PAPERS = 100

# -------------------------------------------------------------------------
# 3. Vector Embeddings & Similarity Search Settings
# -------------------------------------------------------------------------
# Lightweight and high-quality sentence embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Abstract text chunking parameters
CHUNK_SIZE_SENTENCES = 3       # Group 3 sentences together into a chunk
CHUNK_OVERLAP_SENTENCES = 1    # 1 sentence overlap to preserve context

# Number of top evidence passages to feed into the final answer generator
TOP_K_CHUNKS = 4

# -------------------------------------------------------------------------
# 4. Evidence Verification & Abstention Thresholds
# -------------------------------------------------------------------------
# Minimum cosine similarity score required for evidence to be considered relevant.
# Scale: 0.0 (irrelevant) to 1.0 (identical meaning).
MIN_SIMILARITY_THRESHOLD = 0.32

# Standard message displayed when evidence is insufficient or unreliable
ABSTENTION_MESSAGE = "I could not find sufficient reliable evidence in the retrieved literature to provide a confident answer."
NO_EVIDENCE_FOUND_MESSAGE = "No sufficient scientific evidence found for this query."

# -------------------------------------------------------------------------
# 5. LLM (Large Language Model) Settings
# -------------------------------------------------------------------------
# API keys loaded securely from .env (never hardcoded in Python code!)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Model identifiers
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"

# Low temperature ensures the AI stays strictly factual and avoids creative guessing
GENERATION_TEMPERATURE = 0.1


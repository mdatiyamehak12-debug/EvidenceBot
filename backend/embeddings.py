"""
EvidenceBot - Text Embeddings Module
====================================
Uses SentenceTransformers to encode biomedical text passages into dense mathematical
vectors that capture their deep semantic and conceptual meaning.

How Similarity Scores Work:
---------------------------
When text is converted into a vector of numbers, related concepts are placed close together.
By normalizing vectors to unit length (length = 1.0), the dot-product between two vectors
equals their Cosine Similarity:

    Cosine Similarity = (A • B) / (||A|| * ||B||)

Score Interpretation Guide:
- 0.80 - 1.00: Extremely High Relevance (identical or near-identical biomedical assertions)
- 0.60 - 0.79: High Relevance (strong direct evidence addressing the question)
- 0.40 - 0.59: Moderate Relevance (related biological pathway, mechanism, or disease context)
- 0.25 - 0.39: Weak / Peripheral Relevance (mentions shared keywords without answering the inquiry)
- < 0.25: Irrelevant Noise (unrelated biomedical topic)
"""

from typing import List
import numpy as np
import logging

from utils import config

logger = logging.getLogger(__name__)

# Cache the loaded SentenceTransformer model in memory so it is only loaded once
_MODEL_CACHE = None


def get_embedding_model():
    """
    Singleton function that loads and returns the SentenceTransformer model.
    Caches model weights in memory so repeated queries don't incur load delays.
    Supports offline mode seamlessly when weights are already cached locally.
    """
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading SentenceTransformer embedding model: '{config.EMBEDDING_MODEL_NAME}'...")
        try:
            # First try loading with local_files_only if available (avoids network delays)
            _MODEL_CACHE = SentenceTransformer(config.EMBEDDING_MODEL_NAME, local_files_only=True)
            logger.info("Loaded SentenceTransformer from local cache.")
        except Exception:
            try:
                # If not cached locally, load normally
                _MODEL_CACHE = SentenceTransformer(config.EMBEDDING_MODEL_NAME)
                logger.info("SentenceTransformer model loaded successfully.")
            except Exception as err:
                logger.error(f"Failed to load SentenceTransformer: {err}")
                raise RuntimeError(
                    f"SentenceTransformers failed to load. Check installation: {err}"
                )
    return _MODEL_CACHE


def generate_embeddings(texts: List[str]) -> np.ndarray:
    """
    Encodes a list of text strings into unit-normalized dense vector embeddings.
    
    Parameters:
        texts (List[str]): List of sentences or abstract chunks.
        
    Returns:
        np.ndarray: Matrix of shape (len(texts), embedding_dimension), normalized to unit length.
    """
    if not texts:
        return np.empty((0, 384), dtype=np.float32)

    model = get_embedding_model()
    
    # Compute dense embeddings using SentenceTransformers
    raw_vecs = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    embeddings = np.array(raw_vecs, dtype=np.float32)

    # L2-normalization: divide each vector by its Euclidean norm
    # This guarantees that the Inner Product (matrix multiplication) equals Cosine Similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    normalized_embeddings = embeddings / norms

    return normalized_embeddings

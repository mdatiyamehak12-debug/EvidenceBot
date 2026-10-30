"""
EvidenceBot - Vector Store Module (FAISS)
=========================================
Stores and indexes evidence chunk embeddings using FAISS (Facebook AI Similarity Search).
Performs sub-millisecond Cosine Similarity retrieval to match clinical questions
against scientific evidence passages.
"""

from typing import List, Optional
import numpy as np
import logging

from utils import config
from backend.preprocessing import EvidenceChunk
from backend.embeddings import generate_embeddings

logger = logging.getLogger(__name__)


class FaissVectorStore:
    """
    In-memory vector database using FAISS to index and search EvidenceChunks.
    Guarantees fast, exact Cosine Similarity search using normalized IndexFlatIP.
    """

    def __init__(self):
        self.chunks: List[EvidenceChunk] = []
        self.index = None
        self.normalized_vectors: Optional[np.ndarray] = None
        self.dimension: Optional[int] = None

    def add_chunks(self, chunks: List[EvidenceChunk]) -> int:
        """
        Embeds evidence chunks and builds an in-memory FAISS IndexFlatIP index.
        
        Parameters:
            chunks (List[EvidenceChunk]): Chunks to index.
            
        Returns:
            int: Total number of chunks successfully indexed.
        """
        self.chunks = chunks
        if not chunks:
            self.index = None
            self.normalized_vectors = None
            return 0

        # Extract raw text from each chunk
        texts = [c.text for c in chunks]
        logger.info(f"Generating embeddings for {len(texts)} evidence chunks...")
        
        # Unit-normalized vectors (shape: N, D)
        vectors = generate_embeddings(texts)
        self.normalized_vectors = vectors
        self.dimension = vectors.shape[1]

        try:
            import faiss
            # IndexFlatIP computes Inner Product. On normalized vectors, this is Cosine Similarity.
            self.index = faiss.IndexFlatIP(self.dimension)
            self.index.add(vectors)
            logger.info(f"FAISS index built successfully with {self.index.ntotal} vectors.")
        except ImportError:
            logger.warning("FAISS not found; using NumPy matrix dot product fallback.")
            self.index = "NUMPY"

        return len(chunks)

    def similarity_search(
        self,
        query: str,
        top_k: int = config.TOP_K_CHUNKS,
        min_threshold: Optional[float] = None
    ) -> List[EvidenceChunk]:
        """
        Searches the FAISS index for evidence chunks most semantically relevant to the query.
        
        Parameters:
            query (str): The biomedical question.
            top_k (int): Number of top results to return.
            min_threshold (Optional[float]): If specified, drops any chunk with similarity < min_threshold.
            
        Returns:
            List[EvidenceChunk]: Ranked list of evidence chunks with `score` populated.
        """
        if not self.chunks or self.index is None:
            return []

        # 1. Embed and normalize the query vector
        query_vec = generate_embeddings([query])
        k = min(top_k, len(self.chunks))
        results: List[EvidenceChunk] = []

        # 2. Search FAISS index
        if self.index != "NUMPY":
            import faiss
            scores, indices = self.index.search(query_vec, k)
            scores = scores[0]
            indices = indices[0]

            for score, idx in zip(scores, indices):
                if 0 <= idx < len(self.chunks):
                    # Inner product on normalized vectors is Cosine Similarity
                    cos_sim = float(score)
                    
                    # Filter out irrelevant chunks below the threshold if requested
                    if min_threshold is not None and cos_sim < min_threshold:
                        continue

                    c = self.chunks[idx]
                    chunk_with_score = EvidenceChunk(
                        chunk_id=c.chunk_id,
                        pmid=c.pmid,
                        title=c.title,
                        journal=c.journal,
                        year=c.year,
                        text=c.text,
                        url=c.url,
                        score=cos_sim
                    )
                    results.append(chunk_with_score)

        # 3. Fallback: NumPy matrix dot product
        else:
            sims = np.dot(self.normalized_vectors, query_vec.T).flatten()
            top_indices = np.argsort(sims)[::-1][:k]
            for idx in top_indices:
                cos_sim = float(sims[idx])
                if min_threshold is not None and cos_sim < min_threshold:
                    continue

                c = self.chunks[idx]
                chunk_with_score = EvidenceChunk(
                    chunk_id=c.chunk_id,
                    pmid=c.pmid,
                    title=c.title,
                    journal=c.journal,
                    year=c.year,
                    text=c.text,
                    url=c.url,
                    score=cos_sim
                )
                results.append(chunk_with_score)

        return results

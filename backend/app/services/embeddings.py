"""
Embedding generation service
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Initialize model (using a lightweight model for embeddings)
_model = None


def get_embedding_model():
    """Lazy load embedding model"""
    global _model
    if _model is None:
        # Using a lightweight model - can be swapped for instructor/e5-large
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def generate_embedding(text: str) -> List[float]:
    """Generate embedding for a single text"""
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding.tolist()


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts"""
    model = get_embedding_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()


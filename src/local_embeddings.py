from src.base.abstract_cache import EmbeddingModel
import numpy as np
from sentence_transformers import SentenceTransformer

class LocalSentenceTransformer(EmbeddingModel):
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
    
    def get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode([text])[0]
    
    @property
    def dimension(self) -> int:
        return self._dimension

# Пример использования с локальной моделью:
"""
from abstract_cache import AbstractSemanticCache
from openai_implementations import OpenAICompletion
from local_embeddings import LocalSentenceTransformer

cache = AbstractSemanticCache(
    embedding_model=LocalSentenceTransformer(),
    prompt_client=OpenAICompletion(),
    similarity_threshold=0.95
)
"""

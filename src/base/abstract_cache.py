from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Tuple, Any

class EmbeddingModel(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> np.ndarray:
        """Преобразует текст в векторное представление"""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Возвращает размерность эмбеддинга"""
        pass

class PromptClient(ABC):
    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        """Генерирует ответ на промпт"""
        pass

class AbstractSemanticCache:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        prompt_client: PromptClient,
        similarity_threshold: float = 0.95,
        token_per_request: int = None,
    ):
        self.embedding_model = embedding_model
        self.prompt_client = prompt_client
        self.similarity_threshold = similarity_threshold
        self.dimension = embedding_model.dimension

        if token_per_request is None:
            token_per_request = self.dimension
        self.token_per_request = token_per_request
        
        # Инициализация FAISS индекса
        import faiss
        self.index = faiss.IndexFlatL2(self.dimension)
        self.cache: Dict[int, Tuple[str, str]] = {}

    def get_response(self, prompt: str) -> Tuple[str, bool]:
        """Returns (response, cache_hit)"""
        prompt_vector = self.embedding_model.get_embedding(prompt)
        
        if self.index.ntotal > 0:
            D, I = self.index.search(prompt_vector.reshape(1, -1), 1)
            if D[0][0] < (1 - self.similarity_threshold) ** 2:
                cached_prompt, cached_response = self.cache[int(I[0][0])]
                return cached_response, True
        
        # Cache miss
        response = self.prompt_client.get_completion(prompt)
        
        # Store in cache
        index = self.index.ntotal
        self.index.add(prompt_vector.reshape(1, -1))
        self.cache[index] = (prompt, response)
        
        return response, False

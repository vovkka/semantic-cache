from base.abstract_cache import EmbeddingModel, PromptClient
from openai import OpenAI
import numpy as np

class OpenAIEmbedding(EmbeddingModel):
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.client = OpenAI()
        self.model = model
        self._dimension = 1536  # Известная размерность для ada-002
        
    def get_embedding(self, text: str) -> np.ndarray:
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        return np.array(response.data[0].embedding, dtype=np.float32)
    
    @property
    def dimension(self) -> int:
        return self._dimension

class OpenAICompletion(PromptClient):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI()
        self.model = model
    
    def get_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

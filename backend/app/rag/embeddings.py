from typing import List


class EmbeddingService:
    def __init__(self, model_name: str = "text-embedding-3-small"):
        self.model_name = model_name

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [[float(len(text) % 10), float(len(text) % 7), float(len(text) % 5)] for text in texts]

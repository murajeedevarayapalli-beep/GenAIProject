from typing import Any, Dict, List

from app.rag.vector_store import VectorStore


class Retriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self.vector_store.search_documents(query, limit=limit)

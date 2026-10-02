from typing import Any, Dict, List


class VectorStore:
    def __init__(self, collection_name: str = "project_knowledge"):
        self.collection_name = collection_name
        self.documents: List[Dict[str, Any]] = []

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        self.documents.extend(docs)

    def search_documents(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self.documents:
            return []
        query_lower = query.lower()
        return [
            doc for doc in self.documents
            if query_lower in doc.get("content", "").lower()
        ][:limit]

    def delete_document(self, document_id: str) -> None:
        self.documents = [doc for doc in self.documents if doc.get("document_id") != document_id]

    def update_document(self, document_id: str, payload: Dict[str, Any]) -> None:
        for idx, doc in enumerate(self.documents):
            if doc.get("document_id") == document_id:
                self.documents[idx].update(payload)
                return

from __future__ import annotations

from app.rag.vector_store import InMemoryVectorStore, ScoredDocument


class Retriever:
    def __init__(self, vector_store: InMemoryVectorStore) -> None:
        self.vector_store = vector_store

    def retrieve(self, query: str, limit: int = 5) -> list[ScoredDocument]:
        return self.vector_store.search(query=query, limit=limit)


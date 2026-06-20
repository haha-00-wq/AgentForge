from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.rag.embeddings import SimpleEmbeddingModel, cosine_similarity


class Document(BaseModel):
    id: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScoredDocument(Document):
    score: float


class InMemoryVectorStore:
    def __init__(self, embedding_model: SimpleEmbeddingModel | None = None) -> None:
        self.embedding_model = embedding_model or SimpleEmbeddingModel()
        self._documents: list[Document] = []
        self._vectors: dict[str, dict[str, float]] = {}

    def add_documents(self, documents: list[Document]) -> None:
        for document in documents:
            self._documents.append(document)
            self._vectors[document.id] = self.embedding_model.embed(document.content)

    def search(self, query: str, limit: int = 5) -> list[ScoredDocument]:
        query_vector = self.embedding_model.embed(query)
        scored = [
            ScoredDocument(**document.model_dump(), score=cosine_similarity(query_vector, self._vectors[document.id]))
            for document in self._documents
        ]
        scored.sort(key=lambda document: document.score, reverse=True)
        return scored[:limit]


from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.rag.embeddings import SimpleEmbeddingModel, cosine_similarity


class Document(BaseModel):
    """RAG 文档片段模型。

    入参字段:
        id: 文档唯一标识。
        content: 文档正文。
        metadata: 文档元数据，例如 source、url、title。
    """

    id: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ScoredDocument(Document):
    """带检索分数的文档模型。

    入参字段:
        score: 查询与文档的相似度分数。
    """

    score: float


class InMemoryVectorStore:
    """内存向量库默认实现。

    功能:
        保存 Document 和对应向量，支持按查询文本检索相关文档。
        适合测试、示例和无外部依赖的本地运行。
    """

    def __init__(self, embedding_model: SimpleEmbeddingModel | None = None) -> None:
        """初始化内存向量库。

        入参:
            embedding_model: 可选 embedding 模型。不传时使用 SimpleEmbeddingModel。

        出参:
            无。
        """
        self.embedding_model = embedding_model or SimpleEmbeddingModel()
        self._documents: list[Document] = []
        self._vectors: dict[str, dict[str, float]] = {}

    def add_documents(self, documents: list[Document]) -> None:
        """添加文档并建立向量。

        入参:
            documents: 待加入向量库的 Document 列表。

        出参:
            None。
        """
        for document in documents:
            self._documents.append(document)
            self._vectors[document.id] = self.embedding_model.embed(document.content)

    def search(self, query: str, limit: int = 5) -> list[ScoredDocument]:
        """检索相关文档。

        入参:
            query: 查询文本。
            limit: 最多返回的文档数量，默认 5。

        出参:
            list[ScoredDocument]: 按 score 从高到低排序的检索结果。
        """
        query_vector = self.embedding_model.embed(query)
        scored = [
            ScoredDocument(**document.model_dump(), score=cosine_similarity(query_vector, self._vectors[document.id]))
            for document in self._documents
        ]
        scored.sort(key=lambda document: document.score, reverse=True)
        return scored[:limit]

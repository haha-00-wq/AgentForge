from __future__ import annotations

from app.rag.vector_store import InMemoryVectorStore, ScoredDocument


class Retriever:
    """RAG 检索器。

    功能:
        包装向量库，为 Tool、Agent 或 Workflow 提供统一 retrieve 入口。
    """

    def __init__(self, vector_store: InMemoryVectorStore) -> None:
        """初始化检索器。

        入参:
            vector_store: 向量库实例，当前默认使用 InMemoryVectorStore。

        出参:
            无。
        """
        self.vector_store = vector_store

    def retrieve(self, query: str, limit: int = 5) -> list[ScoredDocument]:
        """执行检索。

        入参:
            query: 查询文本。
            limit: 最多返回的文档数量。

        出参:
            list[ScoredDocument]: 检索结果。
        """
        return self.vector_store.search(query=query, limit=limit)

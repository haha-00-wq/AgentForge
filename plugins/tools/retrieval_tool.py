from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from app.protocol import ToolResult
from app.rag import Document, InMemoryVectorStore, Retriever
from app.tools import BaseTool


class RetrievalArgs(BaseModel):
    """RetrievalTool 参数模型。

    入参字段:
        query: 检索查询文本。
        limit: 返回文档数量，范围 1 到 20，默认 5。
    """

    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class RetrievalTool(BaseTool):
    """RAG 检索 Tool。

    功能:
        通过 Retriever 从向量库中检索相关文档，并返回结构化 ToolResult。
    """

    tool_id: ClassVar[str] = "retrieval_tool"
    name: ClassVar[str] = "Retrieval Tool"
    description: ClassVar[str] = "Retrieves relevant documents from a vector store."
    args_schema: ClassVar[type[BaseModel]] = RetrievalArgs

    def __init__(self, retriever: Retriever) -> None:
        """初始化 RetrievalTool。

        入参:
            retriever: RAG 检索器实例。

        出参:
            无。
        """
        self.retriever = retriever

    @classmethod
    def from_documents(cls, documents: list[Document]) -> "RetrievalTool":
        """从文档列表快速创建检索 Tool。

        入参:
            documents: 需要加入内存向量库的 Document 列表。

        出参:
            RetrievalTool: 已绑定 InMemoryVectorStore 的检索 Tool。
        """
        store = InMemoryVectorStore()
        store.add_documents(documents)
        return cls(Retriever(store))

    def run(self, **kwargs) -> ToolResult:
        """执行 RAG 检索。

        入参:
            **kwargs: 必须包含 query，可选 limit，由 RetrievalArgs 校验。

        出参:
            ToolResult: data 中包含 query 和 documents 检索结果。
        """
        args = RetrievalArgs.model_validate(kwargs)
        documents = self.retriever.retrieve(args.query, limit=args.limit)
        return ToolResult(
            tool_id=self.tool_id,
            data={
                "query": args.query,
                "documents": [document.model_dump() for document in documents],
            },
        )

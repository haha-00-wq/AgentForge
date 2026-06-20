from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from app.protocol import ToolResult
from app.rag import Document, InMemoryVectorStore, Retriever
from app.tools import BaseTool


class RetrievalArgs(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=5, ge=1, le=20)


class RetrievalTool(BaseTool):
    tool_id: ClassVar[str] = "retrieval_tool"
    name: ClassVar[str] = "Retrieval Tool"
    description: ClassVar[str] = "Retrieves relevant documents from a vector store."
    args_schema: ClassVar[type[BaseModel]] = RetrievalArgs

    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    @classmethod
    def from_documents(cls, documents: list[Document]) -> "RetrievalTool":
        store = InMemoryVectorStore()
        store.add_documents(documents)
        return cls(Retriever(store))

    def run(self, **kwargs) -> ToolResult:
        args = RetrievalArgs.model_validate(kwargs)
        documents = self.retriever.retrieve(args.query, limit=args.limit)
        return ToolResult(
            tool_id=self.tool_id,
            data={
                "query": args.query,
                "documents": [document.model_dump() for document in documents],
            },
        )


from __future__ import annotations

from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from app.rag import Document, InMemoryVectorStore, ScoredDocument


class KnowledgeFile(BaseModel):
    """知识库文件记录。

    入参字段:
        file_id: 文件 ID。
        kb_id: 知识库 ID。
        filename: 原始文件名。
        chunks: 切片数量。
    """

    file_id: str
    kb_id: str
    filename: str
    chunks: int


class KnowledgeQueryResult(BaseModel):
    """知识库检索结果。

    入参字段:
        question: 用户问题。
        documents: 命中的文档切片列表。
    """

    question: str
    documents: list[ScoredDocument] = Field(default_factory=list)


class InMemoryKnowledgeBaseStore:
    """内存知识库默认实现。

    功能:
        接收上传文件内容，切成 Document 后写入每个 kb_id 独立的内存向量库。
        适合示例和测试，后续可替换为 Chroma、Milvus、Postgres 等持久化实现。
    """

    def __init__(self, chunk_size: int = 800) -> None:
        """初始化知识库 store。

        入参:
            chunk_size: 每个文本切片的最大字符数。

        出参:
            无。
        """
        self.chunk_size = chunk_size
        self._stores: dict[str, InMemoryVectorStore] = {}
        self._files: dict[str, list[KnowledgeFile]] = {}

    def add_text_file(self, kb_id: str, filename: str, content: str) -> list[Document]:
        """上传文本文件内容并写入知识库。

        入参:
            kb_id: 知识库 ID。
            filename: 文件名。
            content: UTF-8 文本内容。

        出参:
            list[Document]: 写入向量库的文档切片。

        异常:
            ValueError: content 为空时抛出。
        """
        normalized = content.strip()
        if not normalized:
            raise ValueError("Uploaded file content is empty.")

        file_id = str(uuid4())
        chunks = self._split_text(normalized)
        documents = [
            Document(
                id=f"{file_id}:{index}",
                content=chunk,
                metadata={
                    "kb_id": kb_id,
                    "file_id": file_id,
                    "filename": filename,
                    "chunk_index": index,
                },
            )
            for index, chunk in enumerate(chunks)
        ]
        self._store_for(kb_id).add_documents(documents)
        self._files.setdefault(kb_id, []).append(
            KnowledgeFile(file_id=file_id, kb_id=kb_id, filename=filename, chunks=len(documents))
        )
        return documents

    def query(self, kb_id: str, question: str, limit: int = 5) -> list[ScoredDocument]:
        """查询知识库。

        入参:
            kb_id: 知识库 ID。
            question: 用户问题。
            limit: 最多返回切片数量。

        出参:
            list[ScoredDocument]: 相关文档切片，按相似度降序排列。
        """
        if kb_id not in self._stores:
            return []
        return self._stores[kb_id].search(question, limit=limit)

    def list_files(self, kb_id: str) -> list[KnowledgeFile]:
        """列出知识库已上传文件。

        入参:
            kb_id: 知识库 ID。

        出参:
            list[KnowledgeFile]: 文件记录列表。
        """
        return list(self._files.get(kb_id, []))

    def _store_for(self, kb_id: str) -> InMemoryVectorStore:
        """获取或创建指定知识库的向量库。

        入参:
            kb_id: 知识库 ID。

        出参:
            InMemoryVectorStore: 对应的内存向量库。
        """
        if kb_id not in self._stores:
            self._stores[kb_id] = InMemoryVectorStore()
        return self._stores[kb_id]

    def _split_text(self, text: str) -> list[str]:
        """将文本切成知识库文档片段。

        入参:
            text: 原始文本。

        出参:
            list[str]: 文本切片列表。
        """
        paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
        chunks: list[str] = []
        for paragraph in paragraphs or [text]:
            for start in range(0, len(paragraph), self.chunk_size):
                chunks.append(paragraph[start : start + self.chunk_size])
        return chunks


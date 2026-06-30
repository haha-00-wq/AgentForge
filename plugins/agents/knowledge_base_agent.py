from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from app.agents import BaseAgent
from app.knowledge import InMemoryKnowledgeBaseStore
from app.protocol import AgentResult, Evidence


class KnowledgeBaseInput(BaseModel):
    """KnowledgeBaseAgent 输入模型。

    入参字段:
        kb_id: 知识库 ID。
        question: 用户问题。
        limit: 检索切片数量。
    """

    kb_id: str = "default"
    question: str = Field(..., min_length=1)
    limit: int = Field(default=3, ge=1, le=10)


class KnowledgeBaseAgent(BaseAgent):
    """知识库问答 Agent。

    功能:
        从指定知识库检索相关文件切片，并基于命中文本生成本地 mock 答案和引用。
    """

    agent_id: ClassVar[str] = "knowledge_base_agent"
    name: ClassVar[str] = "Knowledge Base Agent"
    description: ClassVar[str] = "Answers user questions from uploaded knowledge base files."
    input_schema: ClassVar[type[BaseModel]] = KnowledgeBaseInput

    def __init__(self, knowledge_base: InMemoryKnowledgeBaseStore) -> None:
        """初始化知识库 Agent。

        入参:
            knowledge_base: 共享知识库 store。

        出参:
            无。
        """
        self.knowledge_base = knowledge_base

    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行知识库问答。

        入参:
            state: 必须包含 question，可选 kb_id 和 limit。

        出参:
            AgentResult: data.answer 为答案，data.citations 为引用切片。
        """
        data = KnowledgeBaseInput.model_validate(state)
        documents = self.knowledge_base.query(data.kb_id, data.question, limit=data.limit)
        if not documents:
            return AgentResult(
                agent_id=self.agent_id,
                data={
                    "answer": "知识库中还没有可用于回答该问题的文件内容。",
                    "citations": [],
                },
            )

        top = documents[0]
        citations = [
            {
                "document_id": document.id,
                "filename": document.metadata.get("filename"),
                "chunk_index": document.metadata.get("chunk_index"),
                "score": document.score,
                "content": document.content,
            }
            for document in documents
        ]
        return AgentResult(
            agent_id=self.agent_id,
            data={
                "answer": f"根据上传文件 {top.metadata.get('filename')}：{top.content}",
                "citations": citations,
            },
            evidence=[
                Evidence(
                    source=str(top.metadata.get("filename")),
                    quote=top.content,
                    confidence=max(0.0, min(1.0, top.score)),
                )
            ],
        )


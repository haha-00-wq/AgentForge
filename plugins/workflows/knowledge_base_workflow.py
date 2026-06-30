from __future__ import annotations

from typing import Any, ClassVar

from app.knowledge import InMemoryKnowledgeBaseStore
from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow
from plugins.agents.knowledge_base_agent import KnowledgeBaseAgent


class KnowledgeBaseWorkflow(BaseWorkflow):
    """知识库问答示例 Workflow。

    功能:
        包装 KnowledgeBaseAgent，提供可通过 /workflows/knowledge_base_qa_v1/run 复用的问答流程。
    """

    workflow_id: ClassVar[str] = "knowledge_base_qa_v1"
    name: ClassVar[str] = "Knowledge Base QA Workflow"
    description: ClassVar[str] = "Answers questions from uploaded knowledge base files."

    def __init__(self, knowledge_base: InMemoryKnowledgeBaseStore) -> None:
        """初始化知识库问答 workflow。

        入参:
            knowledge_base: 共享知识库 store。

        出参:
            无。
        """
        self.agent = KnowledgeBaseAgent(knowledge_base)

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行知识库问答。

        入参:
            payload: 必须包含 question，可选 kb_id 和 limit。

        出参:
            WorkflowResult: data 为 KnowledgeBaseAgent 的问答结果。
        """
        result = self.agent.run(payload)
        return WorkflowResult(
            workflow_id=self.workflow_id,
            status=result.status,
            data=result.data,
            steps=[result],
        )


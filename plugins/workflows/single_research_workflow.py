from __future__ import annotations

from typing import Any, ClassVar

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow
from plugins.agents.research_agent import ResearchAgent


class SingleResearchWorkflow(BaseWorkflow):
    """单 Agent 示例 Workflow。

    功能:
        演示最小 workflow 形态：一个 Workflow 只包装一个 Agent。
    """

    workflow_id: ClassVar[str] = "single_research_v1"
    name: ClassVar[str] = "Single Research Workflow"
    description: ClassVar[str] = "Runs only ResearchAgent."

    def __init__(self) -> None:
        """初始化单 Agent workflow。

        入参:
            无。

        出参:
            无。内部创建 ResearchAgent。
        """
        self.research_agent = ResearchAgent()

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行 ResearchAgent。

        入参:
            payload: 必须包含 event_text。

        出参:
            WorkflowResult: data.research 为 ResearchAgent 输出。
        """
        result = self.research_agent.run(payload)
        return WorkflowResult(
            workflow_id=self.workflow_id,
            data={"research": result.data},
            steps=[result],
        )


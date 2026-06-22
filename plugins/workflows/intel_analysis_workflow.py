from __future__ import annotations

from typing import Any, ClassVar

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow
from app.workflows.runner import run_sequential_graph
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent


class IntelAnalysisWorkflow(BaseWorkflow):
    """情报分析示例 Workflow。

    功能:
        使用 LangGraph 顺序编排 ResearchAgent、AnalystAgent、ReviewerAgent。

    输入:
        payload: 必须包含 event_text。

    输出:
        WorkflowResult: data 中包含 research、analysis、review，steps 中包含三个 AgentResult。
    """

    workflow_id: ClassVar[str] = "intel_analysis_v1"
    name: ClassVar[str] = "Intel Analysis Workflow"
    description: ClassVar[str] = "ResearchAgent -> AnalystAgent -> ReviewerAgent."

    def __init__(self) -> None:
        """初始化 Workflow。

        入参:
            无。

        出参:
            无。内部创建三个业务 Agent 实例。
        """
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.reviewer_agent = ReviewerAgent()

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行情报分析流程。

        入参:
            payload: Workflow 输入，必须包含 event_text。

        出参:
            WorkflowResult: 情报分析结构化结果，包含研究、分析、审查三段输出。
        """
        def research_node(state: dict[str, Any]) -> dict[str, Any]:
            """LangGraph 研究节点。

            入参:
                state: 当前 Workflow 状态。

            出参:
                dict[str, Any]: 写入 research 和 steps 后的新状态。
            """
            result = self.research_agent.run(state)
            return {**state, "research": result.data, "steps": [result]}

        def analyst_node(state: dict[str, Any]) -> dict[str, Any]:
            """LangGraph 分析节点。

            入参:
                state: 必须包含 research 和 steps。

            出参:
                dict[str, Any]: 写入 analysis 并追加 steps 后的新状态。
            """
            result = self.analyst_agent.run(state)
            return {**state, "analysis": result.data, "steps": [*state["steps"], result]}

        def reviewer_node(state: dict[str, Any]) -> dict[str, Any]:
            """LangGraph 审查节点。

            入参:
                state: 必须包含 analysis 和 steps。

            出参:
                dict[str, Any]: 写入 review 并追加 steps 后的新状态。
            """
            result = self.reviewer_agent.run(state)
            return {**state, "review": result.data, "steps": [*state["steps"], result]}

        final_state = run_sequential_graph(
            payload,
            [
                ("research", research_node),
                ("analysis", analyst_node),
                ("review", reviewer_node),
            ],
        )

        return WorkflowResult(
            workflow_id=self.workflow_id,
            data={
                "research": final_state["research"],
                "analysis": final_state["analysis"],
                "review": final_state["review"],
            },
            steps=final_state["steps"],
        )

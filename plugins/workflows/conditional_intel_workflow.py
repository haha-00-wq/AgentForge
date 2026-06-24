from __future__ import annotations

from typing import Any, ClassVar, TypedDict

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow, build_conditional_graph, end_path
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent


class ConditionalIntelState(TypedDict, total=False):
    """条件分支情报分析状态。"""

    event_text: str
    research: dict[str, Any]
    analysis: dict[str, Any]
    review: dict[str, Any]
    route: str
    review_status: str
    steps: list[Any]


class ConditionalIntelWorkflow(BaseWorkflow):
    """条件分支情报分析 Workflow。

    功能:
        演示 LangGraph add_conditional_edges。ResearchAgent 后根据 state 路由到
        分析分支或人工审核 pending 分支。
    """

    workflow_id: ClassVar[str] = "conditional_intel_v1"
    name: ClassVar[str] = "Conditional Intel Workflow"
    description: ClassVar[str] = "Routes after research by conditional edges."

    def __init__(self) -> None:
        """初始化条件分支 workflow。

        入参:
            无。

        出参:
            无。内部创建研究、分析、审查 Agent 并编译条件图。
        """
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.reviewer_agent = ReviewerAgent()
        self.graph = build_conditional_graph(
            ConditionalIntelState,
            {
                "research": self._research_node,
                "analysis": self._analysis_node,
                "review": self._review_node,
                "human_review": self._human_review_node,
            },
            entrypoint="research",
            router_node="research",
            route=self._route_after_research,
            path_map={
                "analyze": "analysis",
                "human_review": "human_review",
            },
            edges=[
                ("analysis", "review"),
                ("review", end_path()),
                ("human_review", end_path()),
            ],
        )

    def _research_node(self, state: ConditionalIntelState) -> ConditionalIntelState:
        """研究节点。

        入参:
            state: 初始状态，必须包含 event_text。

        出参:
            ConditionalIntelState: 写入 research、route 和 steps。
        """
        result = self.research_agent.run(state)
        route = "human_review" if "human review" in state["event_text"].lower() else "analyze"
        return {**state, "research": result.data, "route": route, "steps": [result]}

    def _route_after_research(self, state: ConditionalIntelState) -> str:
        """ResearchAgent 后的条件路由函数。

        入参:
            state: 已包含 route 的状态。

        出参:
            str: analyze 或 human_review。
        """
        return state["route"]

    def _analysis_node(self, state: ConditionalIntelState) -> ConditionalIntelState:
        """分析节点。

        入参:
            state: 包含 research 和 steps。

        出参:
            ConditionalIntelState: 写入 analysis 并追加 steps。
        """
        result = self.analyst_agent.run(state)
        return {**state, "analysis": result.data, "steps": [*state["steps"], result]}

    def _review_node(self, state: ConditionalIntelState) -> ConditionalIntelState:
        """审查节点。

        入参:
            state: 包含 analysis 和 steps。

        出参:
            ConditionalIntelState: 写入 review 并追加 steps。
        """
        result = self.reviewer_agent.run(state)
        return {**state, "review": result.data, "steps": [*state["steps"], result]}

    def _human_review_node(self, state: ConditionalIntelState) -> ConditionalIntelState:
        """人工审核 pending 节点。

        入参:
            state: 包含 research。

        出参:
            ConditionalIntelState: 写入 pending_approval 状态。
        """
        return {**state, "review_status": "pending_approval"}

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行条件分支 workflow。

        入参:
            payload: 必须包含 event_text。

        出参:
            WorkflowResult: 分析分支返回 success；人工审核分支返回 pending。
        """
        final_state = self.graph.invoke(payload)
        status = "pending" if final_state.get("review_status") == "pending_approval" else "success"
        return WorkflowResult(
            workflow_id=self.workflow_id,
            status=status,
            data={
                "route": final_state["route"],
                "research": final_state.get("research"),
                "analysis": final_state.get("analysis"),
                "review": final_state.get("review"),
                "review_status": final_state.get("review_status"),
            },
            steps=final_state.get("steps", []),
        )

from __future__ import annotations

from typing import Any, ClassVar, TypedDict

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow, build_conditional_graph, end_path
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.router_agent import RouterAgent


class AgentRouterState(TypedDict, total=False):
    """Agent 路由 Workflow 状态。"""

    event_text: str
    route_hint: str
    router: dict[str, Any]
    research: dict[str, Any]
    analysis: dict[str, Any]
    review_status: str
    finished: bool
    steps: list[Any]


class AgentRouterWorkflow(BaseWorkflow):
    """由 Agent 决策流程走向的 Workflow。

    功能:
        RouterAgent 先输出 data.next，然后 LangGraph conditional edge 根据该决策路由。
    """

    workflow_id: ClassVar[str] = "agent_router_v1"
    name: ClassVar[str] = "Agent Router Workflow"
    description: ClassVar[str] = "Uses RouterAgent output to choose the next branch."

    def __init__(self) -> None:
        """初始化 Agent router workflow。

        入参:
            无。

        出参:
            无。内部创建 RouterAgent、AnalystAgent 并编译条件图。
        """
        self.router_agent = RouterAgent()
        self.analyst_agent = AnalystAgent()
        self.graph = build_conditional_graph(
            AgentRouterState,
            {
                "router": self._router_node,
                "analysis": self._analysis_node,
                "human_review": self._human_review_node,
                "finish": self._finish_node,
            },
            entrypoint="router",
            router_node="router",
            route=self._route_from_agent,
            path_map={
                "analyze": "analysis",
                "human_review": "human_review",
                "finish": "finish",
            },
            edges=[
                ("analysis", end_path()),
                ("human_review", end_path()),
                ("finish", end_path()),
            ],
        )

    def _router_node(self, state: AgentRouterState) -> AgentRouterState:
        """路由 Agent 节点。

        入参:
            state: 包含 event_text，可选 route_hint。

        出参:
            AgentRouterState: 写入 router 决策和 steps。
        """
        result = self.router_agent.run(state)
        return {**state, "router": result.data, "steps": [result]}

    def _route_from_agent(self, state: AgentRouterState) -> str:
        """从 RouterAgent 输出中读取下一跳。

        入参:
            state: 包含 router.next。

        出参:
            str: analyze、human_review 或 finish。
        """
        return state["router"]["next"]

    def _analysis_node(self, state: AgentRouterState) -> AgentRouterState:
        """分析分支节点。

        入参:
            state: 包含 event_text 和 steps。

        出参:
            AgentRouterState: 写入 analysis 并追加 steps。
        """
        research = {"event_text": state["event_text"], "entities": [], "events": []}
        result = self.analyst_agent.run({**state, "research": research})
        return {**state, "research": research, "analysis": result.data, "steps": [*state["steps"], result]}

    def _human_review_node(self, state: AgentRouterState) -> AgentRouterState:
        """人工审核分支节点。

        入参:
            state: 当前状态。

        出参:
            AgentRouterState: 写入 pending_approval。
        """
        return {**state, "review_status": "pending_approval"}

    def _finish_node(self, state: AgentRouterState) -> AgentRouterState:
        """立即结束分支节点。

        入参:
            state: 当前状态。

        出参:
            AgentRouterState: 写入 finished=True。
        """
        return {**state, "finished": True}

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行 Agent 决策路由 workflow。

        入参:
            payload: 必须包含 event_text，可选 route_hint。

        出参:
            WorkflowResult: 根据 RouterAgent 决策返回 success 或 pending。
        """
        final_state = self.graph.invoke(payload)
        status = "pending" if final_state.get("review_status") == "pending_approval" else "success"
        return WorkflowResult(
            workflow_id=self.workflow_id,
            status=status,
            data={
                "router": final_state["router"],
                "research": final_state.get("research"),
                "analysis": final_state.get("analysis"),
                "review_status": final_state.get("review_status"),
                "finished": final_state.get("finished", False),
            },
            steps=final_state.get("steps", []),
        )

from __future__ import annotations

from typing import Any, ClassVar, TypedDict

from langgraph.graph import END, StateGraph

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow


class HumanReviewState(TypedDict, total=False):
    """人工审核 Workflow 状态。

    字段:
        run_id: 被审核运行 ID。
        content: 待审核内容。
        approval: 可选审批结果，包含 approved 和 reviewer。
        review_status: 审核状态。
        reviewer: 审核人。
    """

    run_id: str
    content: str
    approval: dict[str, Any]
    review_status: str
    reviewer: str


class HumanReviewWorkflow(BaseWorkflow):
    """人工审核示例 Workflow。

    功能:
        演示 Human-in-the-loop 的 pending/resume 模式。
        没有 approval 时返回 pending；传入 approval 后返回 approved 或 rejected。
    """

    workflow_id: ClassVar[str] = "human_review_v1"
    name: ClassVar[str] = "Human Review Workflow"
    description: ClassVar[str] = "Demonstrates a LangGraph human-in-the-loop approval checkpoint."

    def __init__(self) -> None:
        """初始化人工审核 LangGraph。

        入参:
            无。

        出参:
            无。内部创建单节点 review_gate 图。
        """
        graph = StateGraph(HumanReviewState)
        graph.add_node("review_gate", self._review_gate)
        graph.set_entry_point("review_gate")
        graph.add_edge("review_gate", END)
        self.graph = graph.compile()

    def _review_gate(self, state: HumanReviewState) -> HumanReviewState:
        """人工审核关口节点。

        入参:
            state: 当前审核状态，可选包含 approval。

        出参:
            HumanReviewState: 没有 approval 时写入 pending_approval；
            有 approval 时写入 approved/rejected 和 reviewer。
        """
        approval = state.get("approval")
        if approval is None:
            return {**state, "review_status": "pending_approval"}
        return {
            **state,
            "review_status": "approved" if approval.get("approved") else "rejected",
            "reviewer": approval.get("reviewer", "unknown"),
        }

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行或恢复人工审核流程。

        入参:
            payload: 包含 run_id、content，可选 approval。

        出参:
            WorkflowResult: 无 approval 时 status=pending；有 approval 时 status=success。
        """
        state = self.graph.invoke(payload)
        status = "pending" if state["review_status"] == "pending_approval" else "success"
        return WorkflowResult(
            workflow_id=self.workflow_id,
            status=status,
            data={
                "run_id": state.get("run_id"),
                "content": state.get("content"),
                "review_status": state["review_status"],
                "reviewer": state.get("reviewer"),
            },
        )

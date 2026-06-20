from __future__ import annotations

from typing import Any, ClassVar, TypedDict

from langgraph.graph import END, StateGraph

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow


class HumanReviewState(TypedDict, total=False):
    run_id: str
    content: str
    approval: dict[str, Any]
    review_status: str
    reviewer: str


class HumanReviewWorkflow(BaseWorkflow):
    workflow_id: ClassVar[str] = "human_review_v1"
    name: ClassVar[str] = "Human Review Workflow"
    description: ClassVar[str] = "Demonstrates a LangGraph human-in-the-loop approval checkpoint."

    def __init__(self) -> None:
        graph = StateGraph(HumanReviewState)
        graph.add_node("review_gate", self._review_gate)
        graph.set_entry_point("review_gate")
        graph.add_edge("review_gate", END)
        self.graph = graph.compile()

    def _review_gate(self, state: HumanReviewState) -> HumanReviewState:
        approval = state.get("approval")
        if approval is None:
            return {**state, "review_status": "pending_approval"}
        return {
            **state,
            "review_status": "approved" if approval.get("approved") else "rejected",
            "reviewer": approval.get("reviewer", "unknown"),
        }

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
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


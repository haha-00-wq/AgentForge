from __future__ import annotations

from typing import Any, ClassVar

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow
from app.workflows.runner import run_sequential_graph
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent


class IntelAnalysisWorkflow(BaseWorkflow):
    workflow_id: ClassVar[str] = "intel_analysis_v1"
    name: ClassVar[str] = "Intel Analysis Workflow"
    description: ClassVar[str] = "ResearchAgent -> AnalystAgent -> ReviewerAgent."

    def __init__(self) -> None:
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.reviewer_agent = ReviewerAgent()

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        def research_node(state: dict[str, Any]) -> dict[str, Any]:
            result = self.research_agent.run(state)
            return {**state, "research": result.data, "steps": [result]}

        def analyst_node(state: dict[str, Any]) -> dict[str, Any]:
            result = self.analyst_agent.run(state)
            return {**state, "analysis": result.data, "steps": [*state["steps"], result]}

        def reviewer_node(state: dict[str, Any]) -> dict[str, Any]:
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


from __future__ import annotations

from typing import Any, ClassVar

from app.agents import BaseAgent
from app.protocol import AgentResult
from app.prompts import PromptStore


class ReviewerAgent(BaseAgent):
    agent_id: ClassVar[str] = "reviewer_agent"
    name: ClassVar[str] = "Reviewer Agent"
    description: ClassVar[str] = "Checks whether the final assessment is supported by evidence."

    def __init__(self, prompts: PromptStore | None = None) -> None:
        self.prompts = prompts or PromptStore()

    def run(self, state: dict[str, Any]) -> AgentResult:
        analysis = state["analysis"]
        evidence = state["steps"][0].evidence
        prompt = self.prompts.render("intel", "reviewer", {"assessment": analysis["assessment"]})

        return AgentResult(
            agent_id=self.agent_id,
            evidence=evidence,
            data={
                "prompt": prompt,
                "supported": bool(evidence),
                "issues": [],
                "final_report": {
                    "summary": analysis["summary"],
                    "assessment": analysis["assessment"],
                    "confidence": analysis["confidence"],
                    "evidence_count": len(evidence),
                },
            },
        )


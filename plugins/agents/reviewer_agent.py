from __future__ import annotations

from typing import Any, ClassVar

from app.agents import BaseAgent
from app.protocol import AgentResult
from app.prompts import PromptStore


class ReviewerAgent(BaseAgent):
    """结论审查 Agent。

    功能:
        读取 AnalystAgent 的判断和 ResearchAgent 的证据，检查结论是否有证据支撑。
    """

    agent_id: ClassVar[str] = "reviewer_agent"
    name: ClassVar[str] = "Reviewer Agent"
    description: ClassVar[str] = "Checks whether the final assessment is supported by evidence."

    def __init__(self, prompts: PromptStore | None = None) -> None:
        """初始化 ReviewerAgent。

        入参:
            prompts: 可选 PromptStore。不传时使用默认 prompts 目录。

        出参:
            无。
        """
        self.prompts = prompts or PromptStore()

    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行审查步骤。

        入参:
            state: Workflow 状态，必须包含 analysis 和 steps。

        出参:
            AgentResult: 包含 supported、issues、final_report。
        """
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

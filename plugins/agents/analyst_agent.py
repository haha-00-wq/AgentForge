from __future__ import annotations

from typing import Any, ClassVar

from app.agents import BaseAgent
from app.protocol import AgentResult
from app.prompts import PromptStore


class AnalystAgent(BaseAgent):
    agent_id: ClassVar[str] = "analyst_agent"
    name: ClassVar[str] = "Analyst Agent"
    description: ClassVar[str] = "Turns extracted research into a structured intelligence assessment."

    def __init__(self, prompts: PromptStore | None = None) -> None:
        self.prompts = prompts or PromptStore()

    def run(self, state: dict[str, Any]) -> AgentResult:
        research = state["research"]
        event_text = research["event_text"]
        prompt = self.prompts.render("intel", "analyst", {"event_text": event_text})

        return AgentResult(
            agent_id=self.agent_id,
            evidence=state["steps"][0].evidence,
            data={
                "prompt": prompt,
                "summary": event_text,
                "key_entities": research["entities"],
                "assessment": "The event is directly supported by the provided source text.",
                "confidence": 0.82,
            },
        )


from __future__ import annotations

from typing import Any, ClassVar

from app.agents import BaseAgent
from app.protocol import AgentResult
from app.prompts import PromptStore


class AnalystAgent(BaseAgent):
    """情报分析 Agent。

    功能:
        读取 ResearchAgent 的输出，生成摘要、关键实体、判断和置信度。
    """

    agent_id: ClassVar[str] = "analyst_agent"
    name: ClassVar[str] = "Analyst Agent"
    description: ClassVar[str] = "Turns extracted research into a structured intelligence assessment."

    def __init__(self, prompts: PromptStore | None = None) -> None:
        """初始化 AnalystAgent。

        入参:
            prompts: 可选 PromptStore。不传时使用默认 prompts 目录。

        出参:
            无。
        """
        self.prompts = prompts or PromptStore()

    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行分析步骤。

        入参:
            state: Workflow 状态，必须包含 research 和 steps。

        出参:
            AgentResult: 包含 summary、key_entities、assessment、confidence。
        """
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

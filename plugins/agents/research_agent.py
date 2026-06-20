from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import BaseModel

from app.agents import BaseAgent
from app.protocol import AgentResult, Evidence
from app.prompts import PromptStore
from plugins.tools.search_tool import SearchTool


class ResearchInput(BaseModel):
    event_text: str


class ResearchAgent(BaseAgent):
    agent_id: ClassVar[str] = "research_agent"
    name: ClassVar[str] = "Research Agent"
    description: ClassVar[str] = "Extracts entities, event facts, and supporting evidence."
    input_schema: ClassVar[type[BaseModel]] = ResearchInput

    def __init__(self, prompts: PromptStore | None = None) -> None:
        self.prompts = prompts or PromptStore()
        self.search_tool = SearchTool()

    def run(self, state: dict[str, Any]) -> AgentResult:
        event_text = ResearchInput.model_validate(state).event_text
        entities = sorted(set(re.findall(r"\b[A-Z][A-Za-z0-9&.-]*(?:\s+[A-Z][A-Za-z0-9&.-]*)*", event_text)))
        search_result = self.search_tool.run(query=event_text)
        prompt = self.prompts.render("intel", "research", {"event_text": event_text})

        return AgentResult(
            agent_id=self.agent_id,
            data={
                "prompt": prompt,
                "event_text": event_text,
                "entities": entities,
                "events": [{"summary": event_text, "type": "reported_event"}],
                "search": search_result.data,
            },
            evidence=[Evidence(source="input.event_text", quote=event_text, confidence=0.9)],
        )


from __future__ import annotations

import re
from typing import Any, ClassVar

from pydantic import BaseModel

from app.agents import BaseAgent
from app.protocol import AgentResult, Evidence
from app.prompts import PromptStore
from plugins.tools.search_tool import SearchTool


class ResearchInput(BaseModel):
    """ResearchAgent 输入模型。

    入参字段:
        event_text: 待分析的事件文本。
    """

    event_text: str


class ResearchAgent(BaseAgent):
    """情报研究 Agent。

    功能:
        从事件文本中提取实体、事件和证据，并调用 SearchTool 生成 mock 检索结果。

    输入:
        state: 至少包含 event_text。

    输出:
        AgentResult.data 包含 prompt、event_text、entities、events、search。
    """

    agent_id: ClassVar[str] = "research_agent"
    name: ClassVar[str] = "Research Agent"
    description: ClassVar[str] = "Extracts entities, event facts, and supporting evidence."
    input_schema: ClassVar[type[BaseModel]] = ResearchInput

    def __init__(self, prompts: PromptStore | None = None) -> None:
        """初始化 ResearchAgent。

        入参:
            prompts: 可选 PromptStore。不传时使用默认 prompts 目录。

        出参:
            无。内部创建 SearchTool。
        """
        self.prompts = prompts or PromptStore()
        self.search_tool = SearchTool()

    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行研究步骤。

        入参:
            state: Workflow 状态，必须包含 event_text。

        出参:
            AgentResult: 包含提取实体、事件、搜索结果和证据的结构化结果。
        """
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

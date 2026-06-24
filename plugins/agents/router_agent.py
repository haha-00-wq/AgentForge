from __future__ import annotations

from typing import Any, ClassVar, Literal

from pydantic import BaseModel, Field

from app.agents import BaseAgent
from app.protocol import AgentResult


RouteDecision = Literal["analyze", "human_review", "finish"]


class RouterInput(BaseModel):
    """RouterAgent 输入模型。

    入参字段:
        event_text: 事件文本。
        route_hint: 可选路由提示，用于测试或外部系统指定流程走向。
    """

    event_text: str
    route_hint: RouteDecision | None = Field(default=None)


class RouterAgent(BaseAgent):
    """流程路由 Agent。

    功能:
        根据输入状态决定下一步 workflow 走向。当前使用 deterministic 规则，
        后续可替换为 LLM structured output。
    """

    agent_id: ClassVar[str] = "router_agent"
    name: ClassVar[str] = "Router Agent"
    description: ClassVar[str] = "Decides the next workflow branch."
    input_schema: ClassVar[type[BaseModel]] = RouterInput

    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行路由决策。

        入参:
            state: Workflow 状态，必须包含 event_text，可选 route_hint。

        出参:
            AgentResult: data.next 表示下一跳，取值 analyze、human_review、finish。
        """
        data = RouterInput.model_validate(state)
        decision = data.route_hint or self._decide_from_text(data.event_text)
        return AgentResult(
            agent_id=self.agent_id,
            data={
                "next": decision,
                "reason": f"Route selected by {'route_hint' if data.route_hint else 'text rule'}.",
            },
        )

    def _decide_from_text(self, event_text: str) -> RouteDecision:
        """根据文本规则决定下一跳。

        入参:
            event_text: 事件文本。

        出参:
            RouteDecision: 包含 human review 时走人工审核；包含 finish 时结束；否则分析。
        """
        lowered = event_text.lower()
        if "human review" in lowered or "manual review" in lowered:
            return "human_review"
        if "finish" in lowered or "no analysis" in lowered:
            return "finish"
        return "analyze"


from __future__ import annotations

from app.agents.base import BaseAgent


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> BaseAgent:
        return self._agents[agent_id]

    def list(self) -> list[dict[str, str]]:
        return [agent.metadata() for agent in self._agents.values()]


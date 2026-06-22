from __future__ import annotations

from app.agents.base import BaseAgent


class AgentRegistry:
    """Agent 注册表。

    功能:
        保存 Agent 实例，并提供按 agent_id 获取、列表展示等能力。

    典型使用位置:
        app/core/plugin_loader.py 注册插件；API 路由读取列表。
    """

    def __init__(self) -> None:
        """初始化空注册表。

        入参:
            无。

        出参:
            无。内部创建 agent_id 到 BaseAgent 的映射。
        """
        self._agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        """注册 Agent 实例。

        入参:
            agent: BaseAgent 子类实例，必须声明 agent_id。

        出参:
            None。
        """
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> BaseAgent:
        """按 ID 获取 Agent。

        入参:
            agent_id: Agent 唯一标识。

        出参:
            BaseAgent: 已注册的 Agent 实例。

        异常:
            KeyError: agent_id 未注册时抛出。
        """
        return self._agents[agent_id]

    def list(self) -> list[dict[str, str]]:
        """列出所有 Agent 元信息。

        入参:
            无。

        出参:
            list[dict[str, str]]: 每项包含 agent_id、name、description。
        """
        return [agent.metadata() for agent in self._agents.values()]

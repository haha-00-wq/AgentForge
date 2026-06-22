from __future__ import annotations

from dataclasses import dataclass

from app.agents import AgentRegistry
from app.core.plugin_loader import load_agents, load_tools, load_workflows
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry


@dataclass(frozen=True)
class AppContainer:
    """应用运行时容器。

    字段:
        agents: Agent 注册表。
        tools: Tool 注册表。
        workflows: Workflow 注册表。

    用途:
        挂载到 FastAPI app.state.container，供 API 路由查询插件。
    """

    agents: AgentRegistry
    tools: ToolRegistry
    workflows: WorkflowRegistry


def bootstrap() -> AppContainer:
    """初始化平台插件容器。

    入参:
        无。

    出参:
        AppContainer: 包含 Agent、Tool、Workflow 三类注册表。
    """
    return AppContainer(
        agents=load_agents(),
        tools=load_tools(),
        workflows=load_workflows(),
    )

from __future__ import annotations

from dataclasses import dataclass

from app.agents import AgentRegistry
from app.core.plugin_loader import load_agents, load_tools, load_workflows
from app.knowledge import InMemoryKnowledgeBaseStore
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry


@dataclass(frozen=True)
class AppContainer:
    """应用运行时容器。

    字段:
        agents: Agent 注册表。
        tools: Tool 注册表。
        workflows: Workflow 注册表。
        knowledge_base: 共享知识库 store。

    用途:
        挂载到 FastAPI app.state.container，供 API 路由查询插件。
    """

    agents: AgentRegistry
    tools: ToolRegistry
    workflows: WorkflowRegistry
    knowledge_base: InMemoryKnowledgeBaseStore


def bootstrap() -> AppContainer:
    """初始化平台插件容器。

    入参:
        无。

    出参:
        AppContainer: 包含 Agent、Tool、Workflow 三类注册表和共享知识库。
    """
    knowledge_base = InMemoryKnowledgeBaseStore()
    return AppContainer(
        agents=load_agents(knowledge_base),
        tools=load_tools(),
        workflows=load_workflows(knowledge_base),
        knowledge_base=knowledge_base,
    )

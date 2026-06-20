from __future__ import annotations

from dataclasses import dataclass

from app.agents import AgentRegistry
from app.core.plugin_loader import load_agents, load_tools, load_workflows
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry


@dataclass(frozen=True)
class AppContainer:
    agents: AgentRegistry
    tools: ToolRegistry
    workflows: WorkflowRegistry


def bootstrap() -> AppContainer:
    return AppContainer(
        agents=load_agents(),
        tools=load_tools(),
        workflows=load_workflows(),
    )


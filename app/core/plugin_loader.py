from __future__ import annotations

from app.agents import AgentRegistry
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent
from plugins.tools.search_tool import SearchTool
from plugins.workflows.intel_analysis_workflow import IntelAnalysisWorkflow


def load_agents() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(ResearchAgent())
    registry.register(AnalystAgent())
    registry.register(ReviewerAgent())
    return registry


def load_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(SearchTool())
    return registry


def load_workflows() -> WorkflowRegistry:
    registry = WorkflowRegistry()
    registry.register(IntelAnalysisWorkflow())
    return registry


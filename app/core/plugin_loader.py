from __future__ import annotations

from app.agents import AgentRegistry
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent
from plugins.tools.retrieval_tool import RetrievalTool
from plugins.tools.search_tool import SearchTool
from plugins.workflows.human_review_workflow import HumanReviewWorkflow
from plugins.workflows.intel_analysis_workflow import IntelAnalysisWorkflow
from app.rag import Document


def load_agents() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(ResearchAgent())
    registry.register(AnalystAgent())
    registry.register(ReviewerAgent())
    return registry


def load_tools() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(SearchTool())
    registry.register(
        RetrievalTool.from_documents(
            [
                Document(
                    id="default-intel-1",
                    content="OSINTBase supports LangGraph workflows, RAG retrieval, and structured evaluation.",
                    metadata={"source": "builtin"},
                )
            ]
        )
    )
    return registry


def load_workflows() -> WorkflowRegistry:
    registry = WorkflowRegistry()
    registry.register(IntelAnalysisWorkflow())
    registry.register(HumanReviewWorkflow())
    return registry

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
    """加载并注册业务 Agent 插件。

    入参:
        无。

    出参:
        AgentRegistry: 已注册 ResearchAgent、AnalystAgent、ReviewerAgent。
    """
    registry = AgentRegistry()
    registry.register(ResearchAgent())
    registry.register(AnalystAgent())
    registry.register(ReviewerAgent())
    return registry


def load_tools() -> ToolRegistry:
    """加载并注册业务 Tool 插件。

    入参:
        无。

    出参:
        ToolRegistry: 已注册 SearchTool 和默认文档集的 RetrievalTool。
    """
    registry = ToolRegistry()
    registry.register(SearchTool())
    registry.register(
        RetrievalTool.from_documents(
            [
                Document(
                    id="default-intel-1",
                    content="AgentForge supports LangGraph workflows, RAG retrieval, and structured evaluation.",
                    metadata={"source": "builtin"},
                )
            ]
        )
    )
    return registry


def load_workflows() -> WorkflowRegistry:
    """加载并注册业务 Workflow 插件。

    入参:
        无。

    出参:
        WorkflowRegistry: 已注册情报分析和人工审核示例 workflow。
    """
    registry = WorkflowRegistry()
    registry.register(IntelAnalysisWorkflow())
    registry.register(HumanReviewWorkflow())
    return registry

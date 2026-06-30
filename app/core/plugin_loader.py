from __future__ import annotations

from app.agents import AgentRegistry
from app.knowledge import InMemoryKnowledgeBaseStore
from app.tools import ToolRegistry
from app.workflows import WorkflowRegistry
from plugins.agents.knowledge_base_agent import KnowledgeBaseAgent
from plugins.agents.analyst_agent import AnalystAgent
from plugins.agents.research_agent import ResearchAgent
from plugins.agents.reviewer_agent import ReviewerAgent
from plugins.agents.router_agent import RouterAgent
from plugins.tools.retrieval_tool import RetrievalTool
from plugins.tools.search_tool import SearchTool
from plugins.workflows.agent_router_workflow import AgentRouterWorkflow
from plugins.workflows.conditional_intel_workflow import ConditionalIntelWorkflow
from plugins.workflows.human_review_workflow import HumanReviewWorkflow
from plugins.workflows.intel_analysis_workflow import IntelAnalysisWorkflow
from plugins.workflows.knowledge_base_workflow import KnowledgeBaseWorkflow
from plugins.workflows.parallel_intel_workflow import ParallelIntelWorkflow
from plugins.workflows.single_research_workflow import SingleResearchWorkflow
from app.rag import Document


def load_agents(knowledge_base: InMemoryKnowledgeBaseStore | None = None) -> AgentRegistry:
    """加载并注册业务 Agent 插件。

    入参:
        无。

    出参:
        AgentRegistry: 已注册 ResearchAgent、AnalystAgent、ReviewerAgent、RouterAgent、
        KnowledgeBaseAgent。
    """
    knowledge_base = knowledge_base or InMemoryKnowledgeBaseStore()
    registry = AgentRegistry()
    registry.register(ResearchAgent())
    registry.register(AnalystAgent())
    registry.register(ReviewerAgent())
    registry.register(RouterAgent())
    registry.register(KnowledgeBaseAgent(knowledge_base))
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


def load_workflows(knowledge_base: InMemoryKnowledgeBaseStore | None = None) -> WorkflowRegistry:
    """加载并注册业务 Workflow 插件。

    入参:
        无。

    出参:
        WorkflowRegistry: 已注册单 Agent、顺序、条件、Agent 路由、并行、知识库问答和人工审核 workflow。
    """
    knowledge_base = knowledge_base or InMemoryKnowledgeBaseStore()
    registry = WorkflowRegistry()
    registry.register(SingleResearchWorkflow())
    registry.register(IntelAnalysisWorkflow())
    registry.register(ConditionalIntelWorkflow())
    registry.register(AgentRouterWorkflow())
    registry.register(ParallelIntelWorkflow())
    registry.register(KnowledgeBaseWorkflow(knowledge_base))
    registry.register(HumanReviewWorkflow())
    return registry

from __future__ import annotations

from typing import Any, ClassVar, TypedDict

from app.protocol import WorkflowResult
from app.workflows import BaseWorkflow, build_parallel_join_graph
from plugins.agents.research_agent import ResearchAgent


class ParallelIntelState(TypedDict, total=False):
    """并行情报分析 Workflow 状态。"""

    event_text: str
    research: dict[str, Any]
    entity_analysis: dict[str, Any]
    risk_analysis: dict[str, Any]
    source_check: dict[str, Any]
    joined: dict[str, Any]
    steps: list[Any]


class ParallelIntelWorkflow(BaseWorkflow):
    """并行情报分析示例 Workflow。

    功能:
        ResearchAgent 后 fan-out 到实体分析、风险分析、来源检查三个并行节点，
        再进入 join 节点汇总。
    """

    workflow_id: ClassVar[str] = "parallel_intel_v1"
    name: ClassVar[str] = "Parallel Intel Workflow"
    description: ClassVar[str] = "Fans out after research and joins branch outputs."

    def __init__(self) -> None:
        """初始化并行 workflow。

        入参:
            无。

        出参:
            无。内部创建 ResearchAgent 并编译并行图。
        """
        self.research_agent = ResearchAgent()
        self.graph = build_parallel_join_graph(
            ParallelIntelState,
            entrypoint="research",
            entry_node=self._research_node,
            parallel_nodes={
                "entity_analysis": self._entity_analysis_node,
                "risk_analysis": self._risk_analysis_node,
                "source_check": self._source_check_node,
            },
            join_name="join",
            join_node=self._join_node,
        )

    def _research_node(self, state: ParallelIntelState) -> ParallelIntelState:
        """研究入口节点。

        入参:
            state: 必须包含 event_text。

        出参:
            ParallelIntelState: 写入 research 和 steps。
        """
        result = self.research_agent.run(state)
        return {**state, "research": result.data, "steps": [result]}

    def _entity_analysis_node(self, state: ParallelIntelState) -> ParallelIntelState:
        """实体分析并行节点。

        入参:
            state: 包含 research。

        出参:
            ParallelIntelState: 写入 entity_analysis。
        """
        entities = state["research"]["entities"]
        return {"entity_analysis": {"entities": entities, "entity_count": len(entities)}}

    def _risk_analysis_node(self, state: ParallelIntelState) -> ParallelIntelState:
        """风险分析并行节点。

        入参:
            state: 包含 event_text。

        出参:
            ParallelIntelState: 写入 risk_analysis。
        """
        lowered = state["event_text"].lower()
        risk_level = "medium" if "risk" in lowered or "incident" in lowered else "low"
        return {"risk_analysis": {"risk_level": risk_level, "signals": []}}

    def _source_check_node(self, state: ParallelIntelState) -> ParallelIntelState:
        """来源检查并行节点。

        入参:
            state: 包含 research.search.results。

        出参:
            ParallelIntelState: 写入 source_check。
        """
        results = state["research"]["search"]["results"]
        return {"source_check": {"source_count": len(results), "sources": results}}

    def _join_node(self, state: ParallelIntelState) -> ParallelIntelState:
        """并行结果汇总节点。

        入参:
            state: 包含三个并行分支输出。

        出参:
            ParallelIntelState: 写入 joined 汇总信息。
        """
        return {
            "joined": {
                "parallel_branches": ["entity_analysis", "risk_analysis", "source_check"],
                "summary": "Parallel analysis completed.",
            }
        }

    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行并行情报分析 workflow。

        入参:
            payload: 必须包含 event_text。

        出参:
            WorkflowResult: 包含 research、三个并行分支和 joined 汇总结果。
        """
        final_state = self.graph.invoke(payload)
        return WorkflowResult(
            workflow_id=self.workflow_id,
            data={
                "research": final_state["research"],
                "entity_analysis": final_state["entity_analysis"],
                "risk_analysis": final_state["risk_analysis"],
                "source_check": final_state["source_check"],
                "joined": final_state["joined"],
            },
            steps=final_state.get("steps", []),
        )


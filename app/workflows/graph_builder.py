from __future__ import annotations

from typing import Any, Callable, TypedDict

from langgraph.graph import END, StateGraph


class SequentialState(TypedDict, total=False):
    """顺序 Agent 图的共享状态类型。

    字段:
        event_text: 示例 workflow 的原始事件文本。
        research: ResearchAgent 输出数据。
        analysis: AnalystAgent 输出数据。
        review: ReviewerAgent 输出数据。
        steps: AgentResult 执行记录列表。
    """

    event_text: str
    research: dict[str, Any]
    analysis: dict[str, Any]
    review: dict[str, Any]
    steps: list[Any]


def build_sequential_agent_graph(
    nodes: list[tuple[str, Callable[[SequentialState], SequentialState]]],
):
    """构建顺序执行的 LangGraph 图。

    入参:
        nodes: 节点列表。每项是 (节点名称, 节点处理函数)，处理函数接收当前 state，
            返回更新后的 state。

    出参:
        CompiledStateGraph: 已编译的 LangGraph 图，可调用 invoke(payload) 执行。

    执行顺序:
        nodes[0] -> nodes[1] -> ... -> END。
    """
    graph = StateGraph(SequentialState)
    for name, handler in nodes:
        graph.add_node(name, handler)

    graph.set_entry_point(nodes[0][0])
    for index, (name, _) in enumerate(nodes):
        next_name = nodes[index + 1][0] if index + 1 < len(nodes) else END
        graph.add_edge(name, next_name)

    return graph.compile()

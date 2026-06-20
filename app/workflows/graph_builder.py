from __future__ import annotations

from typing import Any, Callable, TypedDict

from langgraph.graph import END, StateGraph


class SequentialState(TypedDict, total=False):
    event_text: str
    research: dict[str, Any]
    analysis: dict[str, Any]
    review: dict[str, Any]
    steps: list[Any]


def build_sequential_agent_graph(
    nodes: list[tuple[str, Callable[[SequentialState], SequentialState]]],
):
    graph = StateGraph(SequentialState)
    for name, handler in nodes:
        graph.add_node(name, handler)

    graph.set_entry_point(nodes[0][0])
    for index, (name, _) in enumerate(nodes):
        next_name = nodes[index + 1][0] if index + 1 < len(nodes) else END
        graph.add_edge(name, next_name)

    return graph.compile()


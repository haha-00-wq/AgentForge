from __future__ import annotations

from typing import Any, Callable

from app.workflows.graph_builder import build_sequential_agent_graph


def run_sequential_graph(
    payload: dict[str, Any],
    nodes: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]],
) -> dict[str, Any]:
    graph = build_sequential_agent_graph(nodes)
    return graph.invoke(payload)


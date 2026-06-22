from __future__ import annotations

from typing import Any, Callable

from app.workflows.graph_builder import build_sequential_agent_graph


def run_sequential_graph(
    payload: dict[str, Any],
    nodes: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]],
) -> dict[str, Any]:
    """运行顺序 LangGraph。

    入参:
        payload: 初始状态，通常来自 Workflow.run(payload) 的入参。
        nodes: 顺序节点列表，每个节点负责读取并更新 state。

    出参:
        dict[str, Any]: LangGraph 执行后的最终 state。
    """
    graph = build_sequential_agent_graph(nodes)
    return graph.invoke(payload)

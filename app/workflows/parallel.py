from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph.graph import END, StateGraph


def build_parallel_join_graph(
    state_schema: type,
    entrypoint: str,
    entry_node: Callable[[dict[str, Any]], dict[str, Any]],
    parallel_nodes: dict[str, Callable[[dict[str, Any]], dict[str, Any]]],
    join_name: str,
    join_node: Callable[[dict[str, Any]], dict[str, Any]],
):
    """构建 fan-out/fan-in 并行 LangGraph。

    入参:
        state_schema: LangGraph StateGraph 使用的状态类型，通常是 TypedDict。
        entrypoint: 入口节点名称。
        entry_node: 入口节点函数。
        parallel_nodes: 并行节点映射，每个节点应写入不同 state key，避免并发冲突。
        join_name: 汇总节点名称。
        join_node: 汇总节点函数。

    出参:
        CompiledStateGraph: 已编译的并行图。执行顺序为 entry -> parallel nodes -> join -> END。
    """
    graph = StateGraph(state_schema)
    graph.add_node(entrypoint, entry_node)
    for name, handler in parallel_nodes.items():
        graph.add_node(name, handler)
    graph.add_node(join_name, join_node)

    graph.set_entry_point(entrypoint)
    for name in parallel_nodes:
        graph.add_edge(entrypoint, name)
    graph.add_edge(list(parallel_nodes), join_name)
    graph.add_edge(join_name, END)
    return graph.compile()


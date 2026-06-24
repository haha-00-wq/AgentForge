from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langgraph.graph import END, StateGraph


def build_conditional_graph(
    state_schema: type,
    nodes: dict[str, Callable[[dict[str, Any]], dict[str, Any]]],
    entrypoint: str,
    router_node: str,
    route: Callable[[dict[str, Any]], str],
    path_map: dict[str, str],
    edges: list[tuple[str, str]] | None = None,
):
    """构建 LangGraph 条件分支图。

    入参:
        state_schema: LangGraph StateGraph 使用的状态类型，通常是 TypedDict。
        nodes: 节点名称到节点函数的映射。
        entrypoint: 入口节点名称。
        router_node: 需要挂载条件边的节点名称。
        route: 路由函数，接收当前 state 并返回 path key。
        path_map: path key 到目标节点名的映射，可将某个 key 映射到 END。
        edges: 可选普通边列表，用于描述条件分支后的后续节点关系。

    出参:
        CompiledStateGraph: 已编译的 LangGraph 条件分支图。
    """
    graph = StateGraph(state_schema)
    for name, handler in nodes.items():
        graph.add_node(name, handler)

    graph.set_entry_point(entrypoint)
    graph.add_conditional_edges(router_node, route, path_map)
    for start, end in edges or []:
        graph.add_edge(start, end)
    return graph.compile()


def end_path() -> str:
    """返回 LangGraph END 常量。

    入参:
        无。

    出参:
        str: LangGraph END 常量，用于 path_map。
    """
    return END

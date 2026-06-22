from __future__ import annotations

from app.tools.base import BaseTool


class ToolRegistry:
    """Tool 注册表。

    功能:
        保存业务 Tool 实例，并提供注册、查询和列表展示能力。
    """

    def __init__(self) -> None:
        """初始化空注册表。

        入参:
            无。

        出参:
            无。内部创建 tool_id 到 BaseTool 的映射。
        """
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """注册 Tool 实例。

        入参:
            tool: BaseTool 子类实例，必须声明 tool_id。

        出参:
            None。
        """
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> BaseTool:
        """按 ID 获取 Tool。

        入参:
            tool_id: Tool 唯一标识。

        出参:
            BaseTool: 已注册的 Tool 实例。

        异常:
            KeyError: tool_id 未注册时抛出。
        """
        return self._tools[tool_id]

    def list(self) -> list[dict[str, str]]:
        """列出所有 Tool 元信息。

        入参:
            无。

        出参:
            list[dict[str, str]]: 每项包含 tool_id、name、description。
        """
        return [tool.metadata() for tool in self._tools.values()]

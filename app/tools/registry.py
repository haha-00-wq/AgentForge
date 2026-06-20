from __future__ import annotations

from app.tools.base import BaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.tool_id] = tool

    def get(self, tool_id: str) -> BaseTool:
        return self._tools[tool_id]

    def list(self) -> list[dict[str, str]]:
        return [tool.metadata() for tool in self._tools.values()]


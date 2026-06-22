from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import ToolResult


class BaseTool(ABC):
    """业务 Tool 基类。

    子类需要声明:
        tool_id: Tool 唯一标识。
        name: 展示名称。
        description: 功能描述。
        args_schema: 可选的 Pydantic 参数模型，用于参数校验和 LangChain 适配。

    设计目的:
        让业务 Tool 既能被平台注册管理，也能适配为 LangChain Tool。
    """

    tool_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    args_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        """运行 Tool。

        入参:
            **kwargs: Tool 的业务参数，通常由 args_schema 校验。

        出参:
            ToolResult: Tool 的结构化执行结果。
        """

    def metadata(self) -> dict[str, str]:
        """返回 Tool 元信息。

        入参:
            无。

        出参:
            dict[str, str]: 包含 tool_id、name、description，用于 /tools API。
        """
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
        }

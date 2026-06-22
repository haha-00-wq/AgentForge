from __future__ import annotations

import json
from typing import Any

from langchain_core.tools import StructuredTool

from app.tools.base import BaseTool


def to_langchain_tool(tool: BaseTool) -> StructuredTool:
    """将平台业务 Tool 适配为 LangChain StructuredTool。

    入参:
        tool: BaseTool 子类实例。会读取 tool_id、description、args_schema，
            并在调用时转发到 tool.run(**kwargs)。

    出参:
        StructuredTool: LangChain 可调用的工具对象。invoke 后返回 JSON 字符串。
    """

    def _invoke(**kwargs: Any) -> str:
        """LangChain Tool 内部调用函数。

        入参:
            **kwargs: LangChain 传入的工具参数。

        出参:
            str: ToolResult.data 序列化后的 JSON 字符串。
        """
        result = tool.run(**kwargs)
        return json.dumps(result.data, ensure_ascii=False)

    return StructuredTool.from_function(
        func=_invoke,
        name=tool.tool_id,
        description=tool.description,
        args_schema=tool.args_schema,
    )

from __future__ import annotations

import json
from typing import Any

from langchain_core.tools import StructuredTool

from app.tools.base import BaseTool


def to_langchain_tool(tool: BaseTool) -> StructuredTool:
    def _invoke(**kwargs: Any) -> str:
        result = tool.run(**kwargs)
        return json.dumps(result.data, ensure_ascii=False)

    return StructuredTool.from_function(
        func=_invoke,
        name=tool.tool_id,
        description=tool.description,
        args_schema=tool.args_schema,
    )


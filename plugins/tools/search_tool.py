from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from app.protocol import ToolResult
from app.tools import BaseTool


class SearchArgs(BaseModel):
    """SearchTool 参数模型。

    入参字段:
        query: 搜索查询文本，不能为空。
    """

    query: str = Field(..., min_length=1)


class SearchTool(BaseTool):
    """Mock 搜索 Tool。

    功能:
        为示例和测试提供不依赖外部搜索服务的固定搜索结果。
    """

    tool_id: ClassVar[str] = "search_tool"
    name: ClassVar[str] = "Search Tool"
    description: ClassVar[str] = "Mock search tool used by examples and tests."
    args_schema: ClassVar[type[BaseModel]] = SearchArgs

    def run(self, **kwargs) -> ToolResult:
        """执行 mock 搜索。

        入参:
            **kwargs: 必须包含 query，会由 SearchArgs 校验。

        出参:
            ToolResult: data 中包含 query 和 results 列表。
        """
        args = SearchArgs.model_validate(kwargs)
        return ToolResult(
            tool_id=self.tool_id,
            data={
                "query": args.query,
                "results": [
                    {
                        "title": "Mock intelligence source",
                        "snippet": f"Result for {args.query}",
                        "url": "mock://search/result/1",
                    }
                ],
            },
        )

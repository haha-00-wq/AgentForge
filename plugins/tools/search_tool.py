from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, Field

from app.protocol import ToolResult
from app.tools import BaseTool


class SearchArgs(BaseModel):
    query: str = Field(..., min_length=1)


class SearchTool(BaseTool):
    tool_id: ClassVar[str] = "search_tool"
    name: ClassVar[str] = "Search Tool"
    description: ClassVar[str] = "Mock search tool used by examples and tests."
    args_schema: ClassVar[type[BaseModel]] = SearchArgs

    def run(self, **kwargs) -> ToolResult:
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


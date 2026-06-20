from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import ToolResult


class BaseTool(ABC):
    tool_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    args_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        """Run the business tool and return a structured result."""

    def metadata(self) -> dict[str, str]:
        return {
            "tool_id": self.tool_id,
            "name": self.name,
            "description": self.description,
        }


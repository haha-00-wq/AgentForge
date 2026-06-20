from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import AgentResult


class BaseAgent(ABC):
    agent_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[type[BaseModel] | None] = None
    output_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, state: dict[str, Any]) -> AgentResult:
        """Run the agent with workflow state and return structured output."""

    def metadata(self) -> dict[str, str]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
        }


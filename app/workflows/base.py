from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import WorkflowResult


class BaseWorkflow(ABC):
    workflow_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    state_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """Run the workflow and return a structured result."""

    def metadata(self) -> dict[str, str]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
        }


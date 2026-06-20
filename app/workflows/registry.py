from __future__ import annotations

from app.workflows.base import BaseWorkflow


class WorkflowRegistry:
    def __init__(self) -> None:
        self._workflows: dict[str, BaseWorkflow] = {}

    def register(self, workflow: BaseWorkflow) -> None:
        self._workflows[workflow.workflow_id] = workflow

    def get(self, workflow_id: str) -> BaseWorkflow:
        return self._workflows[workflow_id]

    def list(self) -> list[dict[str, str]]:
        return [workflow.metadata() for workflow in self._workflows.values()]


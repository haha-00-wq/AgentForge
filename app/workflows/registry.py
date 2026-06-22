from __future__ import annotations

from app.workflows.base import BaseWorkflow


class WorkflowRegistry:
    """Workflow 注册表。

    功能:
        保存业务 Workflow 实例，并为 API 层提供查询和列表能力。
    """

    def __init__(self) -> None:
        """初始化空注册表。

        入参:
            无。

        出参:
            无。内部创建 workflow_id 到 BaseWorkflow 的映射。
        """
        self._workflows: dict[str, BaseWorkflow] = {}

    def register(self, workflow: BaseWorkflow) -> None:
        """注册 Workflow 实例。

        入参:
            workflow: BaseWorkflow 子类实例，必须声明 workflow_id。

        出参:
            None。
        """
        self._workflows[workflow.workflow_id] = workflow

    def get(self, workflow_id: str) -> BaseWorkflow:
        """按 ID 获取 Workflow。

        入参:
            workflow_id: Workflow 唯一标识。

        出参:
            BaseWorkflow: 已注册的 Workflow 实例。

        异常:
            KeyError: workflow_id 未注册时抛出。
        """
        return self._workflows[workflow_id]

    def list(self) -> list[dict[str, str]]:
        """列出所有 Workflow 元信息。

        入参:
            无。

        出参:
            list[dict[str, str]]: 每项包含 workflow_id、name、description。
        """
        return [workflow.metadata() for workflow in self._workflows.values()]

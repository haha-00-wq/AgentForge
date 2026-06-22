from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import WorkflowResult


class BaseWorkflow(ABC):
    """业务 Workflow 基类。

    子类需要声明:
        workflow_id: Workflow 唯一标识。
        name: 展示名称。
        description: 功能描述。
        state_schema: 可选的 Pydantic 状态模型。

    设计目的:
        统一 Workflow 的运行入口、元数据和结构化返回协议。
    """

    workflow_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    state_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> WorkflowResult:
        """运行 Workflow。

        入参:
            payload: 外部传入的业务输入，通常来自 API body 或测试用例。

        出参:
            WorkflowResult: Workflow 的结构化执行结果。
        """

    def metadata(self) -> dict[str, str]:
        """返回 Workflow 元信息。

        入参:
            无。

        出参:
            dict[str, str]: 包含 workflow_id、name、description，用于 /workflows API。
        """
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
        }

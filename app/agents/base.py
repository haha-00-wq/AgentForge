from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel

from app.protocol import AgentResult


class BaseAgent(ABC):
    """业务 Agent 基类。

    子类需要声明:
        agent_id: Agent 唯一标识，供注册表和 Workflow 引用。
        name: 展示名称。
        description: 功能描述。
        input_schema: 可选的 Pydantic 输入模型。
        output_schema: 可选的 Pydantic 输出模型。

    设计目的:
        统一 Agent 的元数据、输入校验入口和结构化输出协议。
    """

    agent_id: ClassVar[str]
    name: ClassVar[str]
    description: ClassVar[str]
    input_schema: ClassVar[type[BaseModel] | None] = None
    output_schema: ClassVar[type[BaseModel] | None] = None

    @abstractmethod
    def run(self, state: dict[str, Any]) -> AgentResult:
        """运行 Agent。

        入参:
            state: Workflow 当前状态。通常包含原始输入、上游 Agent 输出、
                steps 执行记录等上下文。

        出参:
            AgentResult: 当前 Agent 的结构化执行结果。
        """

    def metadata(self) -> dict[str, str]:
        """返回 Agent 元信息。

        入参:
            无。

        出参:
            dict[str, str]: 包含 agent_id、name、description，用于 /agents API。
        """
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
        }

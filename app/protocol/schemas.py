from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Status = Literal["success", "error", "pending"]


class Evidence(BaseModel):
    """证据模型。

    入参字段:
        source: 证据来源，例如 input.event_text、网页 URL、数据库记录 ID。
        quote: 支撑结论的原文片段。
        confidence: 证据置信度，范围 0 到 1，默认 0.8。

    出参:
        Pydantic 模型实例，可序列化为 dict/json，通常挂在 AgentResult.evidence 中。
    """

    source: str
    quote: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class Artifact(BaseModel):
    """产物模型。

    入参字段:
        artifact_id: 产物唯一标识。
        type: 产物类型，例如 report、table、image、file。
        uri: 可选的外部或本地资源地址。
        data: 结构化产物内容。

    出参:
        Pydantic 模型实例，通常用于 Agent 或 Workflow 输出附件。
    """

    artifact_id: str
    type: str
    uri: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    """Agent 统一输出协议。

    入参字段:
        agent_id: Agent 唯一标识。
        status: 执行状态，支持 success、error、pending。
        data: Agent 的结构化业务输出。
        evidence: Agent 使用或生成的证据列表。
        artifacts: Agent 生成的文件、报告等产物列表。
        error: 失败时的错误信息。

    出参:
        Pydantic 模型实例，会被 Workflow、API、测试和评估复用。
    """

    agent_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    error: str | None = None


class ToolResult(BaseModel):
    """Tool 统一输出协议。

    入参字段:
        tool_id: Tool 唯一标识。
        status: 执行状态，支持 success、error、pending。
        data: Tool 返回的结构化数据。
        error: 失败时的错误信息。

    出参:
        Pydantic 模型实例，可被业务层直接使用，也可经 adapter 转给 LangChain。
    """

    tool_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class WorkflowResult(BaseModel):
    """Workflow 统一输出协议。

    入参字段:
        workflow_id: Workflow 唯一标识。
        status: 执行状态，支持 success、error、pending。
        data: Workflow 最终结构化输出。
        steps: Workflow 中各 Agent 的执行结果。
        artifacts: Workflow 生成的产物列表。
        error: 失败时的错误信息。

    出参:
        Pydantic 模型实例，通常作为 API 响应体和持久化记录内容。
    """

    workflow_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    steps: list[AgentResult] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    error: str | None = None


class EvaluationResult(BaseModel):
    """评估结果模型。

    入参字段:
        case_id: 评估用例 ID。
        status: 评估状态，支持 success、error、pending。
        score: 评分，范围 0 到 1。
        details: 评分细节，例如命中的字段、期望值和实际值。

    出参:
        Pydantic 模型实例，用于批量评估 CLI、测试和报告生成。
    """

    case_id: str
    status: Status = "success"
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    details: dict[str, Any] = Field(default_factory=dict)

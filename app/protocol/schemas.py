from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Status = Literal["success", "error"]


class Evidence(BaseModel):
    source: str
    quote: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class Artifact(BaseModel):
    artifact_id: str
    type: str
    uri: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    agent_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    error: str | None = None


class ToolResult(BaseModel):
    tool_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class WorkflowResult(BaseModel):
    workflow_id: str
    status: Status = "success"
    data: dict[str, Any] = Field(default_factory=dict)
    steps: list[AgentResult] = Field(default_factory=list)
    artifacts: list[Artifact] = Field(default_factory=list)
    error: str | None = None


class EvaluationResult(BaseModel):
    case_id: str
    status: Status = "success"
    score: float = Field(default=1.0, ge=0.0, le=1.0)
    details: dict[str, Any] = Field(default_factory=dict)


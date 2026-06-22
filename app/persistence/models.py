from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class RunRecord(BaseModel):
    """Workflow 运行记录。

    入参字段:
        run_id: 运行 ID。
        workflow_id: Workflow 唯一标识。
        status: 运行状态。
        payload: 运行输入。
        result: 运行输出。
        created_at: 创建时间，默认当前 UTC 时间。
    """

    run_id: str
    workflow_id: str
    status: str
    payload: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CacheEntry(BaseModel):
    """缓存记录。

    入参字段:
        key: 缓存键。
        value: 缓存值，使用结构化字典。
        created_at: 创建时间。
    """

    key: str
    value: dict[str, Any]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class QueueItem(BaseModel):
    """队列任务记录。

    入参字段:
        item_id: 队列项 ID。
        payload: 任务负载。
        status: 队列状态，默认 queued。
        created_at: 创建时间。
    """

    item_id: str
    payload: dict[str, Any] = Field(default_factory=dict)
    status: str = "queued"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

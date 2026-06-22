from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

from app.core.config import Settings


def configure_tracing(settings: Settings | None = None) -> None:
    """配置 LangSmith tracing 环境变量。

    入参:
        settings: 可选 Settings。不传时自动读取环境变量和 .env。

    出参:
        None。langsmith_tracing 为 false 时不做任何操作。
    """
    settings = settings or Settings()
    if not settings.langsmith_tracing:
        return
    os.environ["LANGSMITH_TRACING"] = "true"
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    return


@dataclass
class TraceContext:
    """Tracing 上下文。

    字段:
        run_name: 当前运行名称。
        metadata: 当前运行的元数据。
        enabled: tracing 是否开启。

    用途:
        在 LangSmith 关闭时作为本地 no-op 上下文；开启时保留统一扩展入口。
    """

    run_name: str
    metadata: dict[str, Any] = field(default_factory=dict)
    enabled: bool = False

    def add_metadata(self, metadata: dict[str, Any]) -> None:
        """追加 tracing 元数据。

        入参:
            metadata: 要合并进当前上下文的元数据字典。

        出参:
            None。
        """
        self.metadata.update(metadata)


@contextmanager
def trace_run(
    run_name: str,
    metadata: dict[str, Any] | None = None,
    enabled: bool | None = None,
    settings: Settings | None = None,
) -> Iterator[TraceContext]:
    """创建一次运行的 tracing 上下文。

    入参:
        run_name: 运行名称。
        metadata: 可选初始元数据。
        enabled: 可选显式开关。不传时使用 Settings.langsmith_tracing。
        settings: 可选 Settings 配置对象。

    出参:
        Iterator[TraceContext]: 上下文管理器中可用的 TraceContext。
    """
    settings = settings or Settings()
    tracing_enabled = settings.langsmith_tracing if enabled is None else enabled
    if tracing_enabled:
        configure_tracing(settings)
    yield TraceContext(run_name=run_name, metadata=dict(metadata or {}), enabled=tracing_enabled)

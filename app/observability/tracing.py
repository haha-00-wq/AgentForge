from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator

from app.core.config import Settings


def configure_tracing(settings: Settings | None = None) -> None:
    settings = settings or Settings()
    if not settings.langsmith_tracing:
        return
    os.environ["LANGSMITH_TRACING"] = "true"
    if settings.langsmith_api_key:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    return


@dataclass
class TraceContext:
    run_name: str
    metadata: dict[str, Any] = field(default_factory=dict)
    enabled: bool = False

    def add_metadata(self, metadata: dict[str, Any]) -> None:
        self.metadata.update(metadata)


@contextmanager
def trace_run(
    run_name: str,
    metadata: dict[str, Any] | None = None,
    enabled: bool | None = None,
    settings: Settings | None = None,
) -> Iterator[TraceContext]:
    settings = settings or Settings()
    tracing_enabled = settings.langsmith_tracing if enabled is None else enabled
    if tracing_enabled:
        configure_tracing(settings)
    yield TraceContext(run_name=run_name, metadata=dict(metadata or {}), enabled=tracing_enabled)

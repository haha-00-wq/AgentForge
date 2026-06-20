from __future__ import annotations

from app.core.config import Settings


def configure_tracing(settings: Settings | None = None) -> None:
    settings = settings or Settings()
    if not settings.langsmith_tracing:
        return
    # LangSmith tracing is enabled through environment variables consumed by LangChain.
    return


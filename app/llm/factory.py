from __future__ import annotations

from app.core.config import Settings
from app.llm.models import create_mock_chat_model


def create_chat_model(settings: Settings | None = None):
    """创建 LangChain ChatModel。

    入参:
        settings: 可选配置对象。不传时自动从环境变量和 .env 构造 Settings。

    出参:
        LangChain ChatModel 实例。默认 LLM_PROVIDER=mock 时返回 FakeListChatModel。

    异常:
        ValueError: llm_provider 不在 mock、openai、openrouter、anthropic、ollama 中时抛出。
        ImportError: 选择真实 provider 但未安装对应 langchain 扩展包时由导入语句抛出。
    """
    settings = settings or Settings()

    if settings.llm_provider == "mock":
        return create_mock_chat_model()

    if settings.llm_provider in {"openai", "openrouter"}:
        from langchain_openai import ChatOpenAI

        base_url = settings.openai_base_url
        api_key = settings.openai_api_key
        if settings.llm_provider == "openrouter":
            base_url = settings.openrouter_base_url
            api_key = settings.openrouter_api_key
        return ChatOpenAI(model=settings.llm_model, api_key=api_key, base_url=base_url)

    if settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(model=settings.llm_model, api_key=settings.anthropic_api_key)

    if settings.llm_provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model=settings.llm_model, base_url=settings.ollama_base_url)

    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")

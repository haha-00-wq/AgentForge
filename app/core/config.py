from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """项目运行配置。

    字段来源:
        默认从环境变量和 .env 文件读取。

    主要配置:
        llm_provider/llm_model: LLM 提供商和模型名。
        *_api_key/base_url: 各模型服务的认证和地址。
        langsmith_*: LangSmith tracing 开关和密钥。
        sqlite_path/postgres_dsn/redis_url: 持久化和缓存扩展配置。
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_provider: str = "mock"
    llm_model: str = "mock-intel"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    anthropic_api_key: str | None = None
    ollama_base_url: str = "http://localhost:11434"
    openrouter_api_key: str | None = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    sqlite_path: str = "data/agentforge.db"
    postgres_dsn: str | None = None
    redis_url: str | None = None

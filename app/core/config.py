from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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

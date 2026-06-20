from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    memory_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    content: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserProfile(BaseModel):
    user_id: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class InMemoryMemoryStore:
    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._memories: dict[str, list[MemoryRecord]] = {}
        self._profiles: dict[str, UserProfile] = {}

    def set_session_state(self, session_id: str, state: dict[str, Any]) -> None:
        self._sessions[session_id] = dict(state)

    def get_session_state(self, session_id: str) -> dict[str, Any]:
        return dict(self._sessions.get(session_id, {}))

    def add_memory(self, user_id: str, content: str, tags: list[str] | None = None) -> MemoryRecord:
        record = MemoryRecord(user_id=user_id, content=content, tags=tags or [])
        self._memories.setdefault(user_id, []).append(record)
        return record

    def search_memories(self, user_id: str, query: str, limit: int = 5) -> list[MemoryRecord]:
        query_lower = query.lower()
        matches = [
            memory
            for memory in self._memories.get(user_id, [])
            if query_lower in memory.content.lower() or any(query_lower in tag.lower() for tag in memory.tags)
        ]
        return matches[:limit]

    def upsert_profile(self, user_id: str, attributes: dict[str, Any]) -> UserProfile:
        existing = self._profiles.get(user_id)
        merged = {**(existing.attributes if existing else {}), **attributes}
        profile = UserProfile(user_id=user_id, attributes=merged)
        self._profiles[user_id] = profile
        return profile

    def get_profile(self, user_id: str) -> UserProfile:
        return self._profiles.get(user_id, UserProfile(user_id=user_id))


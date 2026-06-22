from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    """长期记忆记录。

    入参字段:
        memory_id: 记忆唯一标识，默认自动生成。
        user_id: 用户 ID。
        content: 记忆内容。
        tags: 标签列表，用于粗粒度分类和检索。
        created_at: 创建时间，默认当前 UTC 时间。
    """

    memory_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    content: str
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class UserProfile(BaseModel):
    """用户画像模型。

    入参字段:
        user_id: 用户 ID。
        attributes: 用户画像属性，例如 role、preference、locale。
        updated_at: 更新时间，默认当前 UTC 时间。
    """

    user_id: str
    attributes: dict[str, Any] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class InMemoryMemoryStore:
    """内存 Memory 默认实现。

    功能:
        同时管理 session state、long-term memory 和 user profile。
        适合测试和本地示例，生产环境可替换为数据库或 Redis 实现。
    """

    def __init__(self) -> None:
        """初始化内存 Memory 存储。

        入参:
            无。

        出参:
            无。内部创建 session、memory、profile 三类字典。
        """
        self._sessions: dict[str, dict[str, Any]] = {}
        self._memories: dict[str, list[MemoryRecord]] = {}
        self._profiles: dict[str, UserProfile] = {}

    def set_session_state(self, session_id: str, state: dict[str, Any]) -> None:
        """写入会话状态。

        入参:
            session_id: 会话 ID。
            state: 会话状态字典。

        出参:
            None。
        """
        self._sessions[session_id] = dict(state)

    def get_session_state(self, session_id: str) -> dict[str, Any]:
        """读取会话状态。

        入参:
            session_id: 会话 ID。

        出参:
            dict[str, Any]: 会话状态副本；不存在时返回空字典。
        """
        return dict(self._sessions.get(session_id, {}))

    def add_memory(self, user_id: str, content: str, tags: list[str] | None = None) -> MemoryRecord:
        """追加长期记忆。

        入参:
            user_id: 用户 ID。
            content: 记忆内容。
            tags: 可选标签列表。

        出参:
            MemoryRecord: 新创建的记忆记录。
        """
        record = MemoryRecord(user_id=user_id, content=content, tags=tags or [])
        self._memories.setdefault(user_id, []).append(record)
        return record

    def search_memories(self, user_id: str, query: str, limit: int = 5) -> list[MemoryRecord]:
        """检索用户长期记忆。

        入参:
            user_id: 用户 ID。
            query: 查询文本，当前使用 content/tag 的简单包含匹配。
            limit: 最多返回数量。

        出参:
            list[MemoryRecord]: 匹配到的记忆记录。
        """
        query_lower = query.lower()
        matches = [
            memory
            for memory in self._memories.get(user_id, [])
            if query_lower in memory.content.lower() or any(query_lower in tag.lower() for tag in memory.tags)
        ]
        return matches[:limit]

    def upsert_profile(self, user_id: str, attributes: dict[str, Any]) -> UserProfile:
        """新增或更新用户画像。

        入参:
            user_id: 用户 ID。
            attributes: 要写入的画像属性，会与已有属性合并。

        出参:
            UserProfile: 更新后的用户画像。
        """
        existing = self._profiles.get(user_id)
        merged = {**(existing.attributes if existing else {}), **attributes}
        profile = UserProfile(user_id=user_id, attributes=merged)
        self._profiles[user_id] = profile
        return profile

    def get_profile(self, user_id: str) -> UserProfile:
        """读取用户画像。

        入参:
            user_id: 用户 ID。

        出参:
            UserProfile: 已存在的画像；不存在时返回空 attributes 的默认画像。
        """
        return self._profiles.get(user_id, UserProfile(user_id=user_id))

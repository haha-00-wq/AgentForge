from __future__ import annotations

from langchain_core.language_models.fake_chat_models import FakeListChatModel


def create_mock_chat_model() -> FakeListChatModel:
    return FakeListChatModel(responses=["mock response"])


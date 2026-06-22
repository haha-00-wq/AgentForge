from __future__ import annotations

from langchain_core.language_models.fake_chat_models import FakeListChatModel


def create_mock_chat_model() -> FakeListChatModel:
    """创建本地 mock ChatModel。

    入参:
        无。

    出参:
        FakeListChatModel: 固定返回 mock response，供无 API key 的测试和示例使用。
    """
    return FakeListChatModel(responses=["mock response"])

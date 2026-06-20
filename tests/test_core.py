from app.agents import AgentRegistry
from app.core.config import Settings
from app.llm import create_chat_model
from app.prompts import PromptStore
from plugins.agents.research_agent import ResearchAgent


def test_prompt_store_renders_prompt_file():
    rendered = PromptStore().render(
        "intel",
        "research",
        {"event_text": "Example event"},
    )

    assert "Example event" in rendered


def test_agent_registry_lists_registered_metadata():
    registry = AgentRegistry()
    registry.register(ResearchAgent())

    assert registry.list() == [
        {
            "agent_id": "research_agent",
            "name": "Research Agent",
            "description": "Extracts entities, event facts, and supporting evidence.",
        }
    ]


def test_llm_factory_returns_mock_chat_model_by_default():
    model = create_chat_model(Settings(llm_provider="mock"))

    assert model.invoke("hello").content == "mock response"

from app.knowledge import InMemoryKnowledgeBaseStore
from plugins.agents.knowledge_base_agent import KnowledgeBaseAgent


def test_knowledge_base_agent_answers_with_citations():
    store = InMemoryKnowledgeBaseStore()
    store.add_text_file(
        kb_id="demo",
        filename="agentforge.txt",
        content="AgentForge can answer questions from uploaded knowledge base files.",
    )
    agent = KnowledgeBaseAgent(store)

    result = agent.run({"kb_id": "demo", "question": "What can AgentForge answer from?"})

    assert result.agent_id == "knowledge_base_agent"
    assert result.status == "success"
    assert "uploaded knowledge base files" in result.data["answer"]
    assert result.data["citations"][0]["filename"] == "agentforge.txt"


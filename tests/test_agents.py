from plugins.agents.research_agent import ResearchAgent


def test_research_agent_returns_structured_result():
    agent = ResearchAgent()

    result = agent.run({"event_text": "Acme Corp opened a new lab in Berlin on Monday."})

    assert result.agent_id == "research_agent"
    assert result.status == "success"
    assert result.data["entities"]
    assert result.evidence


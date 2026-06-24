from plugins.workflows.single_research_workflow import SingleResearchWorkflow


def test_single_research_workflow_runs_one_agent():
    result = SingleResearchWorkflow().run({"event_text": "Acme Corp opened a Berlin lab."})

    assert result.workflow_id == "single_research_v1"
    assert result.status == "success"
    assert result.data["research"]["entities"]
    assert [step.agent_id for step in result.steps] == ["research_agent"]


from plugins.workflows.intel_analysis_workflow import IntelAnalysisWorkflow


def test_intel_analysis_workflow_runs_three_agents():
    workflow = IntelAnalysisWorkflow()

    result = workflow.run({"event_text": "Acme Corp opened a new lab in Berlin on Monday."})

    assert result.workflow_id == "intel_analysis_v1"
    assert result.status == "success"
    assert result.data["review"]["supported"] is True
    assert [step.agent_id for step in result.steps] == [
        "research_agent",
        "analyst_agent",
        "reviewer_agent",
    ]


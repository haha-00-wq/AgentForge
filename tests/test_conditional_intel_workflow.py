from plugins.workflows.conditional_intel_workflow import ConditionalIntelWorkflow


def test_conditional_intel_workflow_routes_to_analysis_branch():
    result = ConditionalIntelWorkflow().run({"event_text": "Acme Corp opened a Berlin lab."})

    assert result.workflow_id == "conditional_intel_v1"
    assert result.status == "success"
    assert result.data["route"] == "analyze"
    assert result.data["review"]["supported"] is True


def test_conditional_intel_workflow_routes_to_human_review_branch():
    result = ConditionalIntelWorkflow().run(
        {"event_text": "Acme Corp opened a Berlin lab. needs human review"}
    )

    assert result.status == "pending"
    assert result.data["route"] == "human_review"
    assert result.data["review_status"] == "pending_approval"


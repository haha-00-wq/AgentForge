from plugins.workflows.agent_router_workflow import AgentRouterWorkflow


def test_agent_router_workflow_uses_agent_decision_for_analysis():
    result = AgentRouterWorkflow().run(
        {"event_text": "Acme Corp opened a Berlin lab.", "route_hint": "analyze"}
    )

    assert result.workflow_id == "agent_router_v1"
    assert result.status == "success"
    assert result.data["router"]["next"] == "analyze"
    assert result.data["analysis"]["assessment"]


def test_agent_router_workflow_uses_agent_decision_for_human_review():
    result = AgentRouterWorkflow().run(
        {"event_text": "Acme Corp opened a Berlin lab.", "route_hint": "human_review"}
    )

    assert result.status == "pending"
    assert result.data["router"]["next"] == "human_review"
    assert result.data["review_status"] == "pending_approval"


def test_agent_router_workflow_can_finish_immediately():
    result = AgentRouterWorkflow().run(
        {"event_text": "Acme Corp opened a Berlin lab.", "route_hint": "finish"}
    )

    assert result.status == "success"
    assert result.data["router"]["next"] == "finish"
    assert result.data["finished"] is True


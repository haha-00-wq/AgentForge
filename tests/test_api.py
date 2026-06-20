from fastapi.testclient import TestClient

from app.main import create_app


def test_health_and_catalog_routes():
    client = TestClient(create_app())

    assert client.get("/health").json()["status"] == "ok"
    assert any(item["agent_id"] == "research_agent" for item in client.get("/agents").json())
    assert any(item["tool_id"] == "search_tool" for item in client.get("/tools").json())
    assert any(item["workflow_id"] == "intel_analysis_v1" for item in client.get("/workflows").json())


def test_workflow_run_route():
    client = TestClient(create_app())

    response = client.post(
        "/workflows/intel_analysis_v1/run",
        json={"event_text": "Acme Corp opened a new lab in Berlin on Monday."},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["workflow_id"] == "intel_analysis_v1"
    assert body["status"] == "success"
    assert body["data"]["review"]["supported"] is True

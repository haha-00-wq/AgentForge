from fastapi.testclient import TestClient

from app.main import create_app


def test_knowledge_api_uploads_file_and_answers_question():
    client = TestClient(create_app())

    upload = client.post(
        "/knowledge/demo/files",
        files={"file": ("guide.txt", b"AgentForge supports file upload knowledge base QA.", "text/plain")},
    )
    query = client.post(
        "/knowledge/demo/query",
        json={"question": "What does AgentForge support?"},
    )

    assert upload.status_code == 200
    assert upload.json()["chunks"] == 1
    assert query.status_code == 200
    assert "file upload knowledge base QA" in query.json()["data"]["answer"]

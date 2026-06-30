from app.knowledge import InMemoryKnowledgeBaseStore
from plugins.workflows.knowledge_base_workflow import KnowledgeBaseWorkflow


def test_knowledge_base_workflow_runs_qa_agent():
    store = InMemoryKnowledgeBaseStore()
    store.add_text_file(
        kb_id="demo",
        filename="workflow.txt",
        content="KnowledgeBaseWorkflow wraps KnowledgeBaseAgent for reusable QA.",
    )
    workflow = KnowledgeBaseWorkflow(store)

    result = workflow.run({"kb_id": "demo", "question": "What wraps KnowledgeBaseAgent?"})

    assert result.workflow_id == "knowledge_base_qa_v1"
    assert result.status == "success"
    assert "KnowledgeBaseWorkflow" in result.data["answer"]
    assert [step.agent_id for step in result.steps] == ["knowledge_base_agent"]


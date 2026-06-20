from plugins.workflows.human_review_workflow import HumanReviewWorkflow


def test_human_review_workflow_returns_pending_without_approval():
    result = HumanReviewWorkflow().run({"run_id": "r1", "content": "Needs review"})

    assert result.workflow_id == "human_review_v1"
    assert result.status == "pending"
    assert result.data["review_status"] == "pending_approval"


def test_human_review_workflow_resumes_with_approval():
    result = HumanReviewWorkflow().run(
        {"run_id": "r1", "content": "Needs review", "approval": {"approved": True, "reviewer": "alice"}}
    )

    assert result.status == "success"
    assert result.data["review_status"] == "approved"
    assert result.data["reviewer"] == "alice"

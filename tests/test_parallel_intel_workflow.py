from plugins.workflows.parallel_intel_workflow import ParallelIntelWorkflow


def test_parallel_intel_workflow_runs_fan_out_and_join():
    result = ParallelIntelWorkflow().run({"event_text": "Acme Corp opened a Berlin lab."})

    assert result.workflow_id == "parallel_intel_v1"
    assert result.status == "success"
    assert result.data["entity_analysis"]["entity_count"] > 0
    assert result.data["risk_analysis"]["risk_level"] == "low"
    assert result.data["source_check"]["source_count"] == 1
    assert result.data["joined"]["parallel_branches"] == [
        "entity_analysis",
        "risk_analysis",
        "source_check",
    ]

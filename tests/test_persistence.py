from app.persistence import QueueItem, RunRecord, SQLitePersistenceStore


def test_sqlite_persistence_store_handles_runs_cache_and_queue(tmp_path):
    store = SQLitePersistenceStore(tmp_path / "agentforge.db")

    store.save_run(RunRecord(run_id="r1", workflow_id="intel_analysis_v1", status="success"))
    store.set_cache("answer", {"value": 42})
    store.enqueue(QueueItem(item_id="q1", payload={"task": "review"}))

    assert store.get_run("r1").workflow_id == "intel_analysis_v1"
    assert store.get_cache("answer") == {"value": 42}
    assert store.dequeue().payload == {"task": "review"}
    assert store.dequeue() is None

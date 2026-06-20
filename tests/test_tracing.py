from app.observability.tracing import trace_run


def test_trace_run_is_noop_when_disabled():
    with trace_run("unit-test", metadata={"case": "tracing"}, enabled=False) as trace:
        trace.add_metadata({"status": "ok"})

    assert trace.run_name == "unit-test"
    assert trace.enabled is False
    assert trace.metadata == {"case": "tracing", "status": "ok"}


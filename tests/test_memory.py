from app.memory import InMemoryMemoryStore


def test_memory_store_tracks_session_long_term_memory_and_profile():
    store = InMemoryMemoryStore()

    store.set_session_state("s1", {"topic": "Acme Berlin lab"})
    store.add_memory("u1", "User cares about OSINT workflows", tags=["preference"])
    store.upsert_profile("u1", {"role": "analyst"})

    assert store.get_session_state("s1") == {"topic": "Acme Berlin lab"}
    assert store.search_memories("u1", "OSINT")[0].content == "User cares about OSINT workflows"
    assert store.get_profile("u1").attributes["role"] == "analyst"


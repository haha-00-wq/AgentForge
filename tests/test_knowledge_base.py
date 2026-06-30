from app.knowledge import InMemoryKnowledgeBaseStore


def test_knowledge_base_store_uploads_text_and_retrieves_relevant_chunks():
    store = InMemoryKnowledgeBaseStore()

    documents = store.add_text_file(
        kb_id="demo",
        filename="guide.txt",
        content="AgentForge supports knowledge base upload and question answering.",
    )
    results = store.query("demo", "knowledge base question answering", limit=1)

    assert len(documents) == 1
    assert results[0].metadata["filename"] == "guide.txt"
    assert "question answering" in results[0].content


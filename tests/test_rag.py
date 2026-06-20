from app.rag import Document, InMemoryVectorStore, Retriever
from plugins.tools.retrieval_tool import RetrievalTool


def test_in_memory_vector_store_retrieves_relevant_documents():
    store = InMemoryVectorStore()
    store.add_documents(
        [
            Document(id="1", content="Berlin laboratory opened by Acme Corp", metadata={"city": "Berlin"}),
            Document(id="2", content="Unrelated market update", metadata={"city": "Paris"}),
        ]
    )

    results = Retriever(store).retrieve("Acme Berlin lab", limit=1)

    assert results[0].id == "1"
    assert results[0].metadata["city"] == "Berlin"


def test_retrieval_tool_returns_structured_result():
    tool = RetrievalTool.from_documents(
        [Document(id="intel-1", content="Acme Corp opened a Berlin lab", metadata={"source": "fixture"})]
    )

    result = tool.run(query="Berlin lab")

    assert result.tool_id == "retrieval_tool"
    assert result.status == "success"
    assert result.data["documents"][0]["id"] == "intel-1"


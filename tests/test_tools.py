from app.tools.adapters import to_langchain_tool
from plugins.tools.search_tool import SearchTool


def test_business_tool_can_run_and_adapt_to_langchain_tool():
    tool = SearchTool()

    result = tool.run(query="Acme Berlin lab")
    langchain_tool = to_langchain_tool(tool)

    assert result.tool_id == "search_tool"
    assert result.status == "success"
    assert langchain_tool.name == "search_tool"
    assert "Acme Berlin lab" in langchain_tool.invoke({"query": "Acme Berlin lab"})


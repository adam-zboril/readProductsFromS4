"""Unit test: MCP tool error (simulated API outage) produces a graceful error message."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_api_unavailable_graceful_error():
    """When MCP tool raises an exception, agent returns a graceful error response."""
    mock_tool = MagicMock()
    mock_tool.name = "get_a_product_for_api_product_srv"
    mock_tool.description = "Get product by ID"
    mock_tool.arun = AsyncMock(side_effect=Exception("Connection timeout: S/4HANA API unavailable"))

    from agent import SampleAgent

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_tool])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="What are the details of product TG11?",
            context_id="test-ctx-006",
            tools=[mock_tool]
        )

    # Agent must not crash — it should return a response regardless of tool failure
    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_no_tools_available_graceful_response():
    """When no tools are loaded, agent responds gracefully without tools."""
    from agent import SampleAgent

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="What are the details of product TG11?",
            context_id="test-ctx-007",
            tools=[]
        )

    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None

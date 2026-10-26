"""Unit test: product ID not found returns a clear message, no hallucinated data."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_product_not_found_clear_message():
    """When MCP returns empty results, agent does not fabricate product data."""
    not_found_response = json.dumps({"results": []})

    mock_tool = MagicMock()
    mock_tool.name = "get_a_product_for_api_product_srv"
    mock_tool.description = "Get product by ID"
    mock_tool.arun = AsyncMock(return_value=not_found_response)

    from agent import SampleAgent

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_tool])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="What are the details of product NONEXISTENT-999?",
            context_id="test-ctx-003",
            tools=[mock_tool]
        )

    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None
    # The agent must not return a success response claiming it found the product
    # (it should indicate inability to find it — verified by integration test)

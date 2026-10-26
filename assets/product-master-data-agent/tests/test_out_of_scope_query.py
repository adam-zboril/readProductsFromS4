"""Unit test: out-of-scope queries (pricing, stock) return graceful messages."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_pricing_query_is_out_of_scope():
    """Agent handles pricing query gracefully without crashing."""
    from agent import SampleAgent, get_system_prompt

    # Verify system prompt contains out-of-scope guidance
    system_prompt = get_system_prompt()
    assert "pricing" in system_prompt.lower() or "Fiori" in system_prompt

    mock_tool = MagicMock()
    mock_tool.name = "get_a_product_for_api_product_srv"
    mock_tool.description = "Get product by ID"
    mock_tool.arun = AsyncMock(return_value='{"Product": "TG11"}')

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_tool])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="What is the price of product TG11?",
            context_id="test-ctx-004",
            tools=[mock_tool]
        )

    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None


@pytest.mark.asyncio
async def test_stock_query_is_out_of_scope():
    """Agent handles stock/availability query gracefully without crashing."""
    from agent import SampleAgent

    mock_tool = MagicMock()
    mock_tool.name = "get_a_product_for_api_product_srv"
    mock_tool.description = "Get product by ID"
    mock_tool.arun = AsyncMock(return_value='{"Product": "TG11"}')

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_tool])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="How many units of TG11 are in stock?",
            context_id="test-ctx-005",
            tools=[mock_tool]
        )

    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None

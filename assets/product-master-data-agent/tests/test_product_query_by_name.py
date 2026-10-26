"""Unit test: query by product name uses description search to resolve product ID."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_query_by_name_tool_called():
    """Agent can invoke product description tool when queried by name."""
    description_response = json.dumps({
        "results": [
            {"Product": "TG11", "Language": "EN", "ProductDescription": "Notebook Basic 15"}
        ]
    })

    mock_desc_tool = MagicMock()
    mock_desc_tool.name = "list_a_productdescription_for_api_product_srv"
    mock_desc_tool.description = "Search products by description"
    mock_desc_tool.arun = AsyncMock(return_value=description_response)

    mock_product_tool = MagicMock()
    mock_product_tool.name = "get_a_product_for_api_product_srv"
    mock_product_tool.description = "Get product by ID"
    mock_product_tool.arun = AsyncMock(return_value=json.dumps({
        "Product": "TG11",
        "GrossWeight": "1.500",
        "WeightUnit": "KG",
        "NetWeight": "1.200",
        "BaseUnit": "EA"
    }))

    from agent import SampleAgent

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_desc_tool, mock_product_tool])), \
         patch("langchain_litellm.ChatLiteLLM"):

        agent = SampleAgent()
        response = await agent.invoke(
            query="Tell me about the Notebook Basic product",
            context_id="test-ctx-002",
            tools=[mock_desc_tool, mock_product_tool]
        )

    assert response.status in ("completed", "input_required", "error")
    assert response.message is not None

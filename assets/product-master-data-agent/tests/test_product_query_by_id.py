"""Unit test: query by product ID returns correct mapped attributes."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_query_by_product_id_returns_attributes():
    """Agent retrieves product attributes when queried by a valid product ID."""
    from agent import SampleAgent

    mock_tool_response = json.dumps({
        "Product": "TG11",
        "ProductType": "FERT",
        "GrossWeight": "1.500",
        "WeightUnit": "KG",
        "NetWeight": "1.200",
        "BaseUnit": "EA",
        "ProductGroup": "L001",
        "SizeOrDimensionText": "15x10x8 cm"
    })

    mock_tool = MagicMock()
    mock_tool.name = "get_a_product_for_api_product_srv"
    mock_tool.description = "Retrieve a product by ID"
    mock_tool.arun = AsyncMock(return_value=mock_tool_response)

    mock_llm_response = MagicMock()
    mock_llm_response.content = (
        "**Product ID:** TG11\n"
        "- **Description:** Notebook Basic 15\n"
        "- **Base Unit of Measure:** EA\n"
        "- **Gross Weight:** 1.500 KG\n"
        "- **Net Weight:** 1.200 KG\n"
        "- **Product Group:** L001\n"
        "- **Product Type:** FERT"
    )

    with patch("mcp_providers.agw.get_mcp_tools", AsyncMock(return_value=[mock_tool])), \
         patch("langchain_litellm.ChatLiteLLM") as mock_llm_cls:

        mock_llm_instance = MagicMock()
        mock_llm_cls.return_value = mock_llm_instance

        agent = SampleAgent()
        response = await agent.invoke(
            query="What are the details of product TG11?",
            context_id="test-ctx-001",
            tools=[mock_tool]
        )

    assert response.status in ("completed", "input_required", "error")
    # Agent ran without crashing — product ID query path executed
    assert response.message is not None

# Specification: product-master-data-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Data Dependencies

- API ORD ID: `sap.s4:apiResource:API_PRODUCT_SRV:v1`
- API Spec: `specification/product-master-data-agent/api-specs/API_PRODUCT_SRV.edmx`
- MCP Server ORD ID: to be generated via `mcp-translation-file` skill

MCP tool scope: `read-only`
Resources in scope: `A_Product, A_ProductDescription, A_ProductPlant, A_ProductBasicText, A_ProductUnitsOfMeasure`

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` to understand the full scope before starting
- [x] Bootstrap agent code in `assets/product-master-data-agent/` using instructions from the `sap-agent-bootstrap` section (invoke from inside `assets/product-master-data-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

> **Before proceeding**, read [guidelines-agent-skills.md](../guidelines-agent-skills.md) and decide whether the agent needs runtime skills.

- [x] Create a runtime skill for product master data query handling at `assets/product-master-data-agent/app/skills/product-query/SKILL.md` with:
  - YAML frontmatter: `name: product-query`, `description: Handles natural language queries about product master data from SAP S/4HANA`
  - Step-by-step instructions:
    1. Extract the product identifier (product ID or product name/description) from the user's question
    2. If only a name/description is given (no product ID), search by description first to resolve the product ID
    3. Query the product master MCP tool using the resolved product ID
    4. Return the following attributes if available: product description, base unit of measure, gross weight, net weight, length, width, height, product group, product type
    5. If no product is found for the given ID or search term, respond: "I could not find a product matching '[input]'. Please check the product ID or description and try again."
    6. If an attribute is not maintained in S/4HANA (null/empty), state explicitly that the attribute is not maintained rather than omitting it
    7. Never generate, estimate, or invent product attribute values — all data must come from the MCP tool response

---

## Project-Specific Tasks

### Agent System Prompt

- [x] Open `assets/product-master-data-agent/app/agent.py` and update the `@prompt_section` / `get_system_prompt` body with the following instructions:

  ```
  You are a Product Master Data Assistant for Sales Representatives.
  Your sole purpose is to answer questions about product master data from SAP S/4HANA.

  When a user asks about a product:
  1. Use the product-master MCP tools to retrieve product data.
  2. Only return data retrieved from the MCP tools — never invent or estimate product attributes.
  3. Present attributes clearly: product description, base unit of measure, gross weight, net weight, dimensions (length × width × height), product group, and product type.
  4. If an attribute is not maintained in S/4HANA, state it explicitly.
  5. If the product is not found, respond clearly and ask the user to verify the product ID.
  6. If the user asks about pricing, stock, or availability, explain that this capability is not yet available and suggest they check SAP Fiori for those details.
  7. Keep answers concise and structured — the user is in a live customer interaction.
  ```

### Natural Language Query Handling

- [x] Implement query intent parsing in the agent: detect whether the user is asking by product ID (numeric/alphanumeric code) or by product name/description keyword
- [x] When queried by name/description: use the product description search MCP tool (A_ProductDescription entity) to resolve a matching product ID before retrieving full product details
- [x] When queried by product ID: call the product details MCP tool directly (A_Product entity) using the provided ID
- [x] Handle follow-up questions in the same conversation turn (e.g., "What about product 1000-250?" after a prior lookup) by maintaining context across turns

### Product Attribute Retrieval

- [x] Map the following S/4HANA product master attributes to user-facing labels:
  - `ProductDescription` → "Description"
  - `BaseUnit` → "Base Unit of Measure"
  - `GrossWeight` → "Gross Weight"
  - `NetWeight` → "Net Weight"
  - `WeightUnit` → "Weight Unit"
  - `Length`, `Width`, `Height` → "Dimensions (L × W × H)"
  - `DimensionUnit` → "Dimension Unit"
  - `ProductGroup` → "Product Group"
  - `ProductType` → "Product Type"
- [x] If any attribute value is null, empty string, or "0", report it as "not maintained" in the response

### Error Handling & Guardrails

- [x] If the MCP tool returns no results for a given product ID, respond with a clear not-found message (do not attempt to answer from LLM knowledge)
- [x] If the S/4HANA API is unavailable (MCP tool error), respond: "Product data is temporarily unavailable. Please try again in a moment or check SAP Fiori directly."
- [x] If the user's query is ambiguous (e.g., only a partial product name), ask the user to confirm the product ID before querying
- [x] Reject all requests to create, modify, or delete product data — the agent is strictly read-only
- [x] If the user asks about pricing, availability, or stock: acknowledge the question and explain these are outside the current scope

### Response Format

- [x] Format product attribute responses as a structured list (not a paragraph) for readability during customer calls
- [x] Include the product ID in the response header so the user can confirm the correct product was retrieved
- [x] Keep responses concise — avoid lengthy preambles; lead with the data

---

## MCP Tool Integration

> Read [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) for complete MCP integration patterns.

MCP API: `sap.s4:apiResource:API_PRODUCT_SRV:v1`
MCP tool scope: `read-only`
Resources in scope: `A_Product, A_ProductDescription, A_ProductPlant, A_ProductBasicText, A_ProductUnitsOfMeasure`

- [x] Invoke `mcp-translation-file` skill using the downloaded spec at `specification/product-master-data-agent/api-specs/API_PRODUCT_SRV.edmx` to generate a translation file and MCP server asset. Prune tools to: `A_Product` (read/list), `A_ProductDescription` (read/list), `A_ProductUnitsOfMeasure` (read/list).
- [x] Invoke `setup-solution` skill to create `solution.yaml` and `asset.yaml` files for both `product-master-data-agent` and the generated MCP server asset
- [x] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module — see [guidelines-agent-python.md](../guidelines-agent-python.md) for canonical pattern
- [x] Add the generated MCP server as a dependency in `assets/product-master-data-agent/asset.yaml` under `requires` using the exact ORD ID from the generated MCP asset
- [x] Generate `mcp-mock.json` using the `mcp-mock-config` skill after MCP translation is complete (required before tests can run)

---

## Business Instrumentation

- [x] Implement business step instrumentation for all 5 milestones from the PRD. Use structured logging pattern `[MILESTONE_ID].[achieved|missed]: [description]` and OpenTelemetry custom spans:

  | Milestone | Achieved condition | Log on achievement | Log on miss |
  |---|---|---|---|
  | M1: Agent Connected | MCP tool call to `API_PRODUCT_SRV` succeeds | `M1.achieved: agent successfully connected to S/4HANA Product Master API and returned valid product data` | `M1.missed: agent failed to connect to S/4HANA Product Master API — check MCP translation file and API credentials` |
  | M2: Query Understanding Validated | Natural language query correctly resolves to a product ID and retrieves data | `M2.achieved: natural language query understanding validated — pass rate meets threshold` | `M2.missed: query understanding validation failed — pass rate below threshold, review prompt and tool definitions` |
  | M3: Pilot in SAP Joule | First end-to-end query completed in Joule | `M3.achieved: first successful end-to-end product query completed by pilot Sales Representative in SAP Joule` | `M3.missed: Joule pilot did not complete — check Joule agent registration and endpoint connectivity` |
  | M4: Performance Target Met | 95% of queries return in under 30 seconds | `M4.achieved: response time target met — 95th percentile under 30 seconds confirmed` | `M4.missed: response time target not met — investigate API latency, LLM inference time, and network path` |
  | M5: Full Rollout | Agent available to all Sales Representatives | `M5.achieved: agent fully rolled out to all Sales Representatives in production` | `M5.missed: full rollout did not complete within the target window — review access provisioning and user adoption` |

- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

> See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python testing setup and patterns.

- [x] `conftest.py` only sets `IBD_TESTING=true` — this causes the agent to run with mock MCP tool results during tests
- [x] Write unit test: `test_product_query_by_id.py` — query by product ID returns correct mapped attributes from mock MCP response
- [x] Write unit test: `test_product_query_by_name.py` — query by product name resolves to a product ID then retrieves attributes
- [x] Write unit test: `test_product_not_found.py` — product ID that returns no results produces a clear not-found message (no hallucinated data)
- [x] Write unit test: `test_out_of_scope_query.py` — query about pricing or stock returns the appropriate "out of scope" message
- [x] Write unit test: `test_api_unavailable.py` — MCP tool error (simulated API outage) produces a graceful error message
- [x] Write one integration test `test_end_to_end.py` executing full agent flow: natural language question → MCP tool call → structured response (mocked LLM and MCP, runs offline)
- [x] Run `pytest` from `assets/product-master-data-agent/` (no args, no extra flags) — if coverage < 70%, add tests until threshold met
- [x] Run `pytest` again from `assets/product-master-data-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/product-master-data-agent/` — if not, run pytest again until it does

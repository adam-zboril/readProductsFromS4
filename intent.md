# Product Master Data AI Agent for Sales Representatives

AI agent enabling Sales Representatives to ask natural language questions about product master data from SAP S/4HANA Public Cloud Edition and receive instant, accurate answers via SAP Joule.

## Business challenge

Sales Representatives spend excessive time navigating SAP GUI and Fiori apps to retrieve product master data. The multi-step navigation makes it slow to get basic product details during customer interactions, reducing responsiveness and sales effectiveness. An AI agent embedded in SAP Joule will allow reps to ask questions in plain language and receive immediate, accurate product information.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Time to retrieve product master data | 5 min | < 30 sec | Within 3 months of go-live | Lead to Cash – Product Information Lookup | user |

## Key Milestones

1. **Agent Connected** — Agent deployed and successfully connected to the S/4HANA Product Master API (API_PRODUCT_SRV)
2. **Query Understanding Validated** — Natural language query understanding validated with a representative set of Sales Rep questions
3. **Pilot in SAP Joule** — First successful product data retrieval by a Sales Rep through SAP Joule
4. **Performance Target Met** — Agent responses consistently delivered in under 30 seconds
5. **Full Rollout** — Agent made available to all Sales Representatives

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash

### Process Hierarchy

```
Lead to Cash (E2E)
└── Manage Customers and Channels (generic)
    └── Manage omnichannel experience (BPS-362)
        └── Manage omnichannel product content
```

### Summary

Sales Representatives querying product master data maps to the Lead to Cash E2E — specifically the Manage Customers and Channels phase, where accurate and accessible product content directly enables effective sales execution.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
| ---------------------- | ----------------------- | ---------- | ----------------- | ------------------ | ------------------ | ------------------- | ---- | ------------------- |
| Retrieve product basic details (description, UoM, weight, dimensions) | Product Master (A2X) | `sap.s4:apiResource:API_PRODUCT_SRV:v1` | — | — | — | — | Yes | No pre-built MCP server; MCP translation file must be generated from the OData spec |
| Retrieve product classification and characteristics | Product Master Data Including Classification – Read | `sap.s4:apiResource:API_CLFN_PRODUCT_SRV:v1` | — | — | — | — | Yes | No pre-built MCP server; MCP translation file must be generated |

### Key findings

- The Product Master (A2X) API (`API_PRODUCT_SRV:v1`) is available in the customer's S/4HANA Public Cloud landscape and covers all basic product detail requirements.
- No pre-built MCP server exists for either product master API — custom MCP translation files will be generated from the OData specifications.
- Pricing and availability APIs are either unavailable in this landscape or out of scope for this agent (user selected basic product details only).
- The agent will be surfaced through SAP Joule, aligning with the Sales Rep's existing S/4HANA working environment.
- The Lead to Cash RBA mapping confirms product data access as a core enabler for the omnichannel product content sub-process.
- A Python-based A2A agent is the appropriate solution; no fixed workflow orchestration is needed as queries are open-ended and conversational.

## Recommendations

### AI Agent for Product Master Data Queries in SAP Joule

#### Executive Summary

Python A2A agent answering natural language product queries via Joule

#### Recommended Solution

Build a Python-based AI agent following the A2A protocol. The agent connects to the SAP S/4HANA Product Master OData API via a generated MCP translation file, enabling it to retrieve and interpret product master data in response to natural language questions asked by Sales Representatives inside SAP Joule.

#### Problem Statement

Sales Representatives lose significant time navigating multiple Fiori screens to look up basic product information. This friction slows customer interactions and reduces the quality and speed of sales responses.

#### Affected User Roles

- Sales Representatives

#### Important factors

##### Conversational access to structured SAP data

The agent translates unstructured natural language questions into precise OData queries against the S/4HANA Product Master API, returning clear, human-readable answers without requiring the user to know any SAP transaction codes or navigation paths.

##### Embedded in the Sales Rep's existing workflow

Surfacing the agent in SAP Joule means zero additional context switching — Sales Reps stay in their primary work environment while gaining instant product data access.

#### Potential risks

##### MCP translation accuracy

The MCP translation file is generated from the OData spec. If the spec coverage is incomplete, some product attributes may not be queryable. Mitigation: validate the translation against a representative set of Sales Rep questions during the pilot milestone.

##### API authorization scope

The agent will use the credentials and authorizations of the connected S/4HANA user. Product data visibility will be governed by existing S/4HANA authorization objects — this is expected behavior but should be confirmed during setup.

#### Recommended solution category

AI Agent

#### Intent fit

92%

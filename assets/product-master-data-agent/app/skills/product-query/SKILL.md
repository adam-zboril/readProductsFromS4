---
name: product-query
description: Handles natural language queries about product master data from SAP S/4HANA. Resolves product identifiers, retrieves attributes, and formats responses for Sales Representatives.
allowed-tools:
  - all
---

# Product Query Skill

Follow these steps when a user asks a question about a product:

## Step 1: Identify the Product Identifier

Examine the user's question to determine how the product is referenced:

- **By Product ID**: A numeric or alphanumeric code (e.g., "1000-240", "TG11", "P-100"). Go to Step 2a.
- **By Name or Description**: A descriptive term (e.g., "the blue widget", "standard notebook"). Go to Step 2b.
- **Ambiguous**: If unclear whether it is an ID or name, assume it is a product ID first. If no result is found, retry as a name search.

## Step 2a: Query by Product ID

1. Use the product master MCP tool to fetch product details using the provided product ID.
2. If the product is found, proceed to Step 3.
3. If the product is NOT found, respond: "I could not find a product matching '[input]'. Please check the product ID and try again."
4. Do NOT attempt to answer from general knowledge if the tool returns no result.

## Step 2b: Query by Name or Description

1. Use the product description search MCP tool to find products matching the name or description.
2. If one match is found, use the resolved product ID and proceed to Step 3.
3. If multiple matches are found, list up to 5 results and ask the user to confirm the correct product ID.
4. If no matches are found, respond: "I could not find any products matching '[input]'. Please try a different search term or provide the product ID."

## Step 3: Retrieve and Present Product Attributes

Return the following attributes, formatted as a structured list:

| Attribute | S/4HANA Field | User Label |
|---|---|---|
| Product ID | Product | Product ID |
| Description | ProductDescription | Description |
| Base Unit of Measure | BaseUnit | Base Unit of Measure |
| Gross Weight | GrossWeight + WeightUnit | Gross Weight |
| Net Weight | NetWeight + WeightUnit | Net Weight |
| Dimensions | Length × Width × Height + DimensionUnit | Dimensions |
| Product Group | ProductGroup | Product Group |
| Product Type | ProductType | Product Type |

**For each attribute:**
- If the value is null, empty string, or "0": report as "Not maintained"
- Always include the product ID at the top of the response

## Step 4: Handle Follow-up Questions

If the user asks a follow-up question about the same product (e.g., "What about the weight?"), reuse the product ID from the previous turn without re-querying.

If the user references a different product (e.g., "What about product 1000-250?"), start again from Step 1.

## Out-of-Scope Requests

If the user asks about:
- **Pricing or sales conditions**: Respond "Pricing information is not yet available through this assistant. Please check the Pricing app in SAP Fiori."
- **Stock or availability**: Respond "Stock and availability information is not yet available through this assistant. Please check the Stock Overview app in SAP Fiori."
- **Creating or modifying products**: Respond "I can only retrieve product information. For changes, please use the Manage Products app in SAP Fiori."

### Building a toolkit

We can create different types of LLM-based tools to handle various specialized tasks:

- Transformation Tools: Converting between different data formats and structures
- Analysis Tools: Providing expert insight in specific domains
- Generation Tools: Creating structured content from specifications
- Validation Tools: Checking if content meets specific criteria
- Extraction Tools: Pulling specific information from larger contexts

````
response = generate_response(Prompt(messages=[
                {"role": "system",
                 "content": f"You MUST produce output that adheres to the following JSON schema:\n\n{json.dumps(schema, indent=4)}. Output your JSON in a ```json markdown block."},
                {"role": "user", "content": prompt}
            ]))
````

The agent can use this tool to:

- Extract meeting details from emails, converting them to calendar-ready formats
- Transform unstructured report data into structured analytics inputs
- Convert web page content into structured product or contact information
- Process customer communications into actionable support tickets

When designing our agent’s toolset, we face an important architectural decision regarding data extraction. We can either rely on the agent to use the general-purpose prompt_llm_for_json tool with dynamically generated schemas, or we can create specialized extraction tools with fixed schemas for specific types of documents. This choice reflects a classic tradeoff between flexibility and reliability.

```
# Define a fixed schema for invoice data
    invoice_schema = {
        "type": "object",
        "required": ["invoice_number", "date", "amount"],  # These fields must be present
        "properties": {
            "invoice_number": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "amount": {
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "currency": {"type": "string"}
                },
                "required": ["value", "currency"]
            },
            "vendor": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "tax_id": {"type": "string"},
                    "address": {"type": "string"}
                },
                "required": ["name"]
            },
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "total": {"type": "number"}
                    },
                    "required": ["description", "total"]
                }
            }
        }
    }

    # Create a focused prompt that guides the LLM in invoice extraction
    extraction_prompt = f"""
    Extract invoice information from the following document text.
    Focus on identifying:
    - Invoice number (usually labeled as 'Invoice #', 'Reference', etc.)
    - Date (any dates labeled as 'Invoice Date', 'Issue Date', etc.)
    - Amount (total amount due, including currency)
    - Vendor information (company name, tax ID if present, address)
    - Line items (individual charges and their details)

    Document text:
    {document_text}
    """
```

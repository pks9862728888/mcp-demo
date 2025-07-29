[Instructors gihub repo] (https://github.com/nordquant/mcp-course)

### Environment setup
We will use UV as package manager for Python 
```
pip install uv
```

- To collect all dependencies used in venv
```
pip freeze > requirements.py
```

- To create virtual env with uv
```
uv virtualenv .venv
```

We will use pyproject.toml to specify dependencies.

- To install dependencies:
```
uv sync
```

- To add new dependency:
```
uv add openai
```

- To activate virtual env
```
# On Windows
.venv\Scripts\activate

# If gitbash
source .venv/Scripts/activate
```

- To run a script
```
uv run main.py
```

---
#### MCP architecture
- MCP host: Programs that want to access MCP services like Claude or Cursor
- MCP client: The client module that maintain connection between host and server
- MCP protocol: The language MCP clients and servers use for communication and data passing
- MCP server: Server applications that expose functionalities for LLMs through MCP protocol

#### MCP functionalities
- Tool use, @mcp.tool()
- Resources: Provide LLM with files and assets, @app.list_resouces(), @app.read_resource()
- Prompts: Provide pre-created prompts

Partially supported features:
- Roots: Define which resources to use with MCP
- Sampling: Classic LLM next token prediction service

---
### To add MCP server in Claude desktop
```
{
  "mcpServers": {
    "zapier-mcp": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "<<<Paste the Zapier URL from zapier.com here, something like https://mcp.zapier.com/api/mcp/a/11353467/mcp>>>"
      ]
    }
  }
}
```

## Pydantic
Pydantic is a Python library for data validation and settings management that leverages Python's type annotations. It allows you to define data models using Python classes and automatically checks that any input data matches the structure and types you declare. At its core, Pydantic turns standard type hints into runtime validation rules, reducing manual code for validating and parsing data

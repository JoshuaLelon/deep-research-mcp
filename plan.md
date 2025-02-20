- [ ] Create a new file in the same directory as your multi_agents/main.py. For example, call it mcp_server.py. In that file, put the following code:

```python
# mcp_server.py
import os
import asyncio
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from typing import Any

# Assume multi_agents/main.py has an async function called main() 
# that provides deep research functionality. We'll expose it as a "tool."

# We'll define a tool that calls multi_agents' functionality
# in a simplified way. Adjust argument signatures to match your real code.

def run_deep_research_tool(query: str) -> str:
    """
    Synchronous wrapper for demonstration.
    Replace with the appropriate call to your multi_agents.main() code.
    """
    # Add the real logic or call to multi_agents here.
    # For example:
    # results = asyncio.run(multi_agents.main(query))
    # return results
    return f"Stubbed result for query: {query}"

app = Server("research-tool-server")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="deep_research",
            description="Perform deep research using the multi_agents script",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.Content]:
    if name == "deep_research":
        query = arguments["query"]
        result = run_deep_research_tool(query)
        return [types.TextContent(type="text", text=result)]
    raise ValueError(f"Tool not found: {name}")

# Optional: define resources, prompts, or other capabilities as needed.

async def main():
    # Standard input/output server
    async with stdio_server() as streams:
        await app.run(
            streams[0],
            streams[1],
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

- [ ] Adjust multi_agents/README.md (or create a new one if it doesn’t exist) to describe the new file you just created and its purpose. For example:

```markdown
# multi_agents

## Overview
This directory contains tools to perform deep research using multi-agent architectures.

## Files
- main.py  
  Entry point for the deep research tool, handling orchestrations and environment loading.  
- mcp_server.py  
  MCP server implementation that exposes the research tool as a "deep_research" tool to external MCP clients.

## Usage
You can run the MCP server by calling:
```bash
python mcp_server.py
```
Then an MCP client can discover and invoke "deep_research" as a tool.
```

- [ ] Update the parent directory’s README.md (if one exists and is relevant to the entire project) to mention the multi_agents folder’s new MCP capabilities. For example:

```markdown
# Project Root

## Overview
This project includes a deep research tool in the `multi_agents` folder. It also exposes an MCP server so that external MCP clients can invoke research functionality.

## Directory structure
- multi_agents
  - README.md (details about multi_agents usage)
  - main.py (core logic for deep research)
  - mcp_server.py (MCP server exposing the deep research tool)

## Running the MCP Server
To start the MCP server, just run:
```bash
cd multi_agents
python mcp_server.py
```

```

- [ ] Ensure that your Python environment includes the mcp library (e.g., pip install mcp). If your multi_agents/main.py relies on additional dependencies, include installation steps for those in the README.md files as well.

- [ ] Confirm that when you run python mcp_server.py, the server starts and waits on stdio. Test from any MCP client (e.g., the Inspector or a custom client) to verify that the deep_research tool is discoverable and operational.

That’s it! Once these steps are complete, you’ll have a functional MCP server exposing your “deep research” functionality from multi_agents/main.py via a neat “deep_research” tool.

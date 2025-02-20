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

--

Based on the error and your request, I'll outline a plan to refactor the MCP server to return research results directly to the chat instead of writing to files.

# Refactoring Plan for MCP Deep Research Server

## 1. Modify mcp_server.py
- Remove file system outputs
- Modify the tool to return structured results directly
- Add proper typing for the response format

```typescript:mcp_server.py
# Modify the deep_research tool definition to specify structured output
@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="deep_research",
            description="Perform deep research using multi-agent architecture",
            inputSchema={
                "type": "object",
                "properties": {
                    "tone": {"type": "string"},
                    "query": {"type": "string"},
                },
                "required": ["tone", "query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.Content]:
    if name == "deep_research":
        # Get research results directly without file output
        results = await run_deep_research(arguments["tone"], arguments["query"])
        
        # Format results as text content
        return [types.TextContent(
            type="text",
            text=results
        )]
    raise ValueError(f"Tool not found: {name}")
```

## 2. Modify multi_agents/main.py
```python:multi_agents/main.py
# Replace file writing with direct return
async def main(tone: str, query: str) -> str:
    # ... existing setup code ...
    
    # Instead of writing to files, collect output in a string
    output = []
    
    # Modify research steps to append to output instead of writing files
    for step in research_steps:
        result = await step.execute()
        output.append(result)
    
    # Return formatted results
    return "\n\n".join(output)
```

## 3. Update README.md
```markdown:multi_agents/README.md
# Multi Agents Research Tool

## Updates
- Now returns research results directly to chat
- No longer writes to filesystem
- Structured output format for better readability

## Usage via MCP
The deep_research tool now returns results directly in the chat interface:

Input:
- tone: The desired tone for the response
- query: The research question to investigate

Output:
- Formatted research results returned directly in chat
```

## Implementation Steps:

1. Remove all file writing operations from multi_agents/main.py
2. Modify the agent execution flow to collect results in memory
3. Update the MCP server to properly format and return the results
4. Test the changes using Claude Desktop to verify direct output

## Testing:
1. Run the MCP server
2. Use Claude Desktop to make a research query
3. Verify results appear directly in chat without file system errors
4. Test different query types and response formats

## Error Handling:
- Add proper error handling for memory constraints
- Include progress updates during long-running research
- Format errors as readable messages in chat

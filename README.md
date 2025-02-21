# Deep Research MCP

This repository provides a multi-agent research framework using Python and MCP (Message Control Protocol). The default entrypoint is `mcp_server.py`, which sets up a FastMCP server named **Deep Research** and exposes a tool named `deep_research`.

## Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/deep-research-mcp.git
   cd deep-research-mcp
   ```

2. **Create/Populate Your `.env` File:**
   ```bash
   cp .env.example .env
   # Then edit the new .env file to fill in your secrets and environment variables
   # For example:
   # OPENAI_API_KEY=sk-123-yourkey
   # Additional environment variables can be placed here
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r multi_agents/requirements.txt
   ```

4. Edit your `claude_desktop_config.json` file to include the following:
    ```
    {
        "mcpServers": {
            "deep-research-mcp": {
                "command": "path/to/your/python/interpreter",
                "args": [
                    "/path/to/this/project/deep-research-mcp/mcp_server.py"
                ]
            }
        }
    }
    ```

5. **Run the MCP Server:**
   ```bash
   python mcp_server.py
   ```
   This starts the FastMCP tool server locally. From here, any MCP-compatible client or the CLI can invoke the `deep_research` tool.

## Project Overview

- **multi_agents**  
  - **agents**: Contains the various AI agents (ResearchAgent, EditorAgent, etc.).  
  - **memory**: Typed dictionaries to store research and draft states.  
  - **main.py**: Core logic to load tasks and orchestrate agents.  
  - **README.md**: Additional instructions on usage, file output settings, etc.
- **mcp_server.py**: Main FastMCP server file (entrypoint).
- **utils**: Shared functions and enums used across the codebase.
- **.gitignore**, **requirements.txt**, etc.: Standard setup files.

Below is a copy of the `multi_agents/README.md` in a tree-like structure for reference:

```
multi_agents/
│
├─ README.md
│   └─ (Documentation on file output vs. direct return)
│
├─ agents/
│   ├─ __init__.py
│   ├─ browser.py
│   ├─ researcher.py
│   ├─ editor.py
│   ├─ writer.py
│   ├─ publisher.py
│   └─ ... (other agents)
│
├─ memory/
│   ├─ __init__.py
│   ├─ draft.py
│   └─ research.py
│
├─ main.py
├─ __init__.py
└─ requirements.txt
```
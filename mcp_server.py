from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, Optional
from gpt_researcher.utils.enum import Tone
import asyncio
import os
from dotenv import load_dotenv
from multi_agents.main import run_research_task

# Load environment variables
load_dotenv()

# Create an MCP server named "Deep Research"
mcp = FastMCP("Deep Research")

@mcp.tool()
async def deep_research(
    query: str, 
    tone: str = "objective",
    ctx: Context = None
) -> Dict[Any, Any]:
    """
    Perform deep research on a given query using multiple AI agents.
    
    Args:
        query: The research question or topic to investigate
        tone: Research tone (objective, critical, optimistic, balanced, skeptical)
        ctx: MCP context for progress reporting
        
    Returns:
        A dictionary containing the research results and analysis
    """
    try:
        # Convert tone string to enum
        tone_enum = getattr(Tone, tone.capitalize(), Tone.Objective)
        
        # Define a stream output handler that reports progress via MCP
        async def stream_output(type: str, key: str, value: Any, _):
            if ctx:
                if type == "logs":
                    ctx.info(f"{key}: {value}")
                elif type == "progress":
                    await ctx.report_progress(value, 100)

        # Run the research task
        research_report = await run_research_task(
            query=query,
            websocket=None,  # We're not using websockets in MCP
            stream_output=stream_output,
            tone=tone_enum
        )

        return {
            "status": "success",
            "query": query,
            "tone": tone,
            "report": research_report
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    # Run the server
    mcp.run() 
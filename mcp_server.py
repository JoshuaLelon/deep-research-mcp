from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, Optional
from gpt_researcher.utils.enum import Tone
import asyncio
import os
from dotenv import load_dotenv
from multi_agents.main import run_research_task, run_get_sources

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

@mcp.tool()
async def get_sources(
    query: str
) -> Dict[Any, Any]:
    """
    Take a query and return a list of sources to browse.
    
    Args:
        query: The research question or topic to investigate
        
    Returns:
        A list of sources to browse
    """
    try:
        
        # Define a stream output handler that reports progress via MCP
        # async def stream_output(type: str, key: str, value: Any, _):
        #     if ctx:
        #         if type == "logs":
        #             ctx.info(f"{key}: {value}")
        #         elif type == "progress":
        #             await ctx.report_progress(value, 100)

        # Run the research task
        sources = await run_get_sources(query)

        return {
            "status": "success",
            "query": query,
            "sources": sources
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# @mcp.tool()
# async def outline(
#     sources: list[str]
# ) -> str:
#     """
#     Take a list of sources and return an outline of the research.
    
#     Args:
#         sources: A list of sources to browse
        
#     Returns:
#         A string containing the outline of the research
#     """
#     try:
        
#         # Define a stream output handler that reports progress via MCP
#         async def stream_output(type: str, key: str, value: Any, _):
#             if ctx:
#                 if type == "logs":
#                     ctx.info(f"{key}: {value}")
#                 elif type == "progress":
#                     await ctx.report_progress(value, 100)

#         # Run the research task
#         outline = await get_outline(
#             sources=sources,
#             stream_output=stream_output,
#         )

#         return {
#             "status": "success",
#             "sources": sources,
#             "outline": outline
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }

# @mcp.tool()
# async def draft(
#     outline: str
# ) -> str:
#     """
#     Take an outline and return a draft of the research.
    
#     Args:
#         outline: The outline of the research
        
#     Returns:
#         A string containing the draft of the research
#     """
#     try:
        
#         # Define a stream output handler that reports progress via MCP
#         async def stream_output(type: str, key: str, value: Any, _):
#             if ctx:
#                 if type == "logs":
#                     ctx.info(f"{key}: {value}")
#                 elif type == "progress":
#                     await ctx.report_progress(value, 100)

#         # Run the research task
#         draft = await get_draft(
#             outline=outline,
#             stream_output=stream_output,
#         )

#         return {
#             "status": "success",
#             "outline": outline,
#             "draft": draft
#         }

#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e)
#         }

if __name__ == "__main__":
    # Run the server
    mcp.run() 
from dotenv import load_dotenv
import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from multi_agents.agents import ChiefEditorAgent
import asyncio
import json
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import Tone

# Run with LangSmith if API key is set
if os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
load_dotenv()

def open_task():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to task.json
    task_json_path = os.path.join(current_dir, 'task.json')
    
    with open(task_json_path, 'r') as f:
        task = json.load(f)

    if not task:
        raise Exception("No task found. Please ensure a valid task.json file is present in the multi_agents directory and contains the necessary task information.")

    return task

async def run_research_task(query, websocket=None, stream_output=None, tone=Tone.Objective, headers=None):
    task = open_task()
    task["query"] = query

    chief_editor = ChiefEditorAgent(task, websocket, stream_output, tone, headers)
    try:
        research_report = await chief_editor.run_research_task()
        
        if websocket and stream_output:
            # Format as JSON message
            message = {
                "report": research_report,
                "status": "complete"
            }
            await stream_output("logs", "research_report", message, websocket)
        
        return research_report
    except Exception as e:
        error_msg = {
            "error": str(e),
            "status": "failed"
        }
        if websocket and stream_output:
            await stream_output("logs", "error", error_msg, websocket)
        raise

async def run_get_sources(query, websocket=None, stream_output=None, tone=Tone.Objective, headers=None):
    try:
        # Initialize the researcher
        researcher = GPTResearcher(query=query, report_type="research_report", parent_query="", verbose=False, report_source="web", tone=None, websocket=None, headers=None)
        # Conduct research on the given query
        research_report = await researcher.plan_research()
        return research_report
    except Exception as e:
        error_msg = {
            "error": str(e),
            "status": "failed"
        }
        if websocket and stream_output:
            await stream_output("logs", "error", error_msg, websocket)
        raise

# async def get_outline(sources=sources, websocket=None, stream_output=None, tone=Tone.Objective, headers=None):
#     pass

# async def get_draft(outline=outline, websocket=None, stream_output=None, tone=Tone.Objective, headers=None):
#     pass

async def main():
    task = open_task()

    chief_editor = ChiefEditorAgent(task)
    research_report = await chief_editor.run_research_task(task_id=uuid.uuid4())

    return research_report

if __name__ == "__main__":
    asyncio.run(main())
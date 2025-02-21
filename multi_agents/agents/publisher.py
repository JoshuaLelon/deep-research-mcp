from .utils.file_formats import \
    write_md_to_pdf, \
    write_md_to_word, \
    write_text_to_md

from .utils.views import print_agent_output


class PublisherAgent:
    def __init__(self, output_dir: str, websocket=None, stream_output=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.output_dir = output_dir
        self.headers = headers or {}
        
    async def publish_research_report(self, research_state: dict, publish_formats: dict):
        layout = self.generate_layout(research_state)
        if self.output_dir:
            await self.write_report_by_formats(layout, publish_formats)

        # Return the layout wrapped in a proper structure
        return {
            "content": layout,
            "format": "markdown",
            "metadata": {
                "title": research_state.get("headers", {}).get("title", ""),
                "date": research_state.get("date", "")
            }
        }

    def generate_layout(self, research_state: dict):
        sections = '\n\n'.join(f"{value}"
                                 for subheader in research_state.get("research_data")
                                 for key, value in subheader.items())
        references = '\n'.join(f"{reference}" for reference in research_state.get("sources"))
        headers = research_state.get("headers")
        layout = f"""# {headers.get('title')}
#### {headers.get("date")}: {research_state.get('date')}

## {headers.get("introduction")}
{research_state.get('introduction')}

## {headers.get("table_of_contents")}
{research_state.get('table_of_contents')}

{sections}

## {headers.get("conclusion")}
{research_state.get('conclusion')}

## {headers.get("references")}
{references}
"""
        return layout

    async def write_report_by_formats(self, layout:str, publish_formats: dict):
        if publish_formats.get("pdf"):
            await write_md_to_pdf(layout, self.output_dir)
        if publish_formats.get("docx"):
            await write_md_to_word(layout, self.output_dir)
        if publish_formats.get("markdown"):
            await write_text_to_md(layout, self.output_dir)

    async def run(self, research_state: dict):
        task = research_state.get("task")
        publish_formats = task.get("publish_formats")
        
        if self.websocket and self.stream_output:
            status_msg = {
                "type": "status",
                "message": "Publishing final research report...",
                "progress": 0
            }
            await self.stream_output("logs", "publishing", status_msg, self.websocket)
        else:
            print_agent_output(output="Publishing final research report...", agent="PUBLISHER")
        
        try:
            result = await self.publish_research_report(research_state, publish_formats)
            
            if self.websocket and self.stream_output:
                complete_msg = {
                    "type": "status",
                    "message": "Report published successfully",
                    "progress": 100
                }
                await self.stream_output("logs", "publishing", complete_msg, self.websocket)
            
            return {
                "status": "success",
                "report": result,
                "metadata": {
                    "formats": list(publish_formats.keys()) if publish_formats else ["markdown"]
                }
            }
            
        except Exception as e:
            error_msg = {
                "type": "error",
                "message": f"Error publishing report: {str(e)}"
            }
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "error", error_msg, self.websocket)
            raise

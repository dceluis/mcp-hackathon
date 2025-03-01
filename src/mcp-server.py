import asyncio
import json
import mcp.types as types
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount  # Import Mount
from typing import List, Union
import uvicorn

# --- Configuration (Load from a config file in a real implementation) ---
SERVER_NAME = "Tasker-MCP-Bridge"
SERVER_PORT = 8000  # Or any available port

# --- Tool Definitions (Hardcoded for simplicity, could be loaded from a file) ---
TOOLS = {
    "tasker_run_task": types.Tool(
        name="tasker_run_task",
        description="Run a Tasker task.",
        inputSchema={
            "type": "object",
            "properties": {
                "task_name": {"type": "string", "description": "The name of the Tasker task to run."},
                "parameters": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional parameters to pass to the Tasker task."
                }
            },
            "required": ["task_name"]
        }
    ),
     "get_variable": types.Tool( #add another tool for demonstration
        name="get_variable",
        description="Gets the value of a Tasker global variable.",
        inputSchema={
            "type": "object",
            "properties": {
                "variable_name": {"type": "string", "description": "The name of the Tasker global variable (e.g., '%MYVAR')."}
            },
            "required": ["variable_name"]
        }
    )
}


app = Server(SERVER_NAME)
sse = SseServerTransport("/messages/")

@app.list_tools()
async def list_tools() -> list[types.Tool]:
  return list(TOOLS.values())

@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]: # Correct return type
    if name == "tasker_run_task":
        task_name = arguments.get("task_name")
        parameters = arguments.get("parameters", [])

        if not task_name:
            raise ValueError("task_name is required")
        return await run_tasker_task(task_name, parameters) # Correct return type
    if name == "get_variable":
         variable_name = arguments.get("variable_name")
         if not variable_name:
            raise ValueError("variable_name is required")
         return await get_tasker_variable(variable_name) # Correct return type

    raise ValueError(f"Unknown tool: {name}")



async def run_tasker_task(task_name: str, parameters: list[str]) ->  List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Sends an intent to Tasker to run a task."""
    #This is a placeholder - you will need a way to send intents!

    command = [
      "termux-toast", # Using termux-toast as a placeholder for intent sending
       task_name
    ]
    #add parameters to command
    for p in parameters:
      command.append(p)

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    _, stderr = await process.communicate() #stdout is not used

    if process.returncode != 0:
        #Error handling: return an error result to MCP Client
        return [types.TextContent(type="text", text=f"Error running Tasker task: {stderr.decode()}")]

    #Success:
    return [types.TextContent(type="text", text="Tasker task executed successfully.")]

async def get_tasker_variable(variable_name:str) ->  List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
  #use perform task and %par1 as input, then return as output
  result = await run_tasker_task("Get Global Variable", [variable_name])
  return result

async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Mount("/messages/", app=sse.handle_post_message),
    ]
)

async def main():
    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=SERVER_PORT, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())

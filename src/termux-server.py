import asyncio
import sys
import mcp.types as types
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount  # Import Mount
from typing import List, Union
import uvicorn
import logging

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO, stream=sys.stderr,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-server")

SERVER_NAME = "Tasker-MCP-Bridge"
SERVER_PORT = 8000

TOOLS = [
    types.Tool(
        name="tasker_get_battery_level",
        description="Returns the current battery percentage.",
        inputSchema={"type": "object", "properties": {}}
    ),
    types.Tool(
        name="tasker_lamp_on",
        description="Turns the bedroom lamp on.",
        inputSchema={"type": "object", "properties": {}}
    ),
    types.Tool(
        name="tasker_lamp_off",
        description="Turns the bedroom lamp off.",
        inputSchema={"type": "object", "properties": {}}
    ),
    types.Tool(
        name="tasker_toggle_torch",
        description="Turns flashlight on or off.",
        inputSchema={
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["on", "off"]}
            },
            "required": ["state"]
        }
    ),
    types.Tool(
        name="tasker_toggle_wifi",
        description="Turns WiFi on or off.",
        inputSchema={
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["on", "off"]}
            },
            "required": ["state"]
        }
    ),
    types.Tool(
        name="tasker_get_location",
        description="Retrieves the current GPS coordinates.",
        inputSchema={"type": "object", "properties": {}}
    ),
    types.Tool(
        name="tasker_flash_text",
        description="Displays a short message using tasker Flash action.",
        inputSchema={
            "type": "object",
            "properties": {
                "Text": {"type": "string", "description": "The text to show on the user phone."}
            },
            "required": ["text"]
        }
    ),
    types.Tool(
        name="tasker_send_sms",
        description="Sends an SMS message.",
        inputSchema={
            "type": "object",
            "properties": {
                "number": {"type": "string", "description": "Recipient phone number."},
                "message": {"type": "string", "description": "Message content."}
            },
            "required": ["number", "message"]
        }
    ),
]

app = Server(SERVER_NAME)
sse = SseServerTransport("/messages/")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
  return list(TOOLS)

#In call tool:
@app.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    logger.info(f"call_tool: name={name}, arguments={arguments}")

    if name == "tasker_get_battery_level":
        filtered_arguments = { key: val for key, val in arguments.items() if key in [] }
        return await run_tasker_task("MCP Get Battery Level", {})
    elif name == "tasker_toggle_wifi":
        filtered_arguments = { key: val for key, val in arguments.items() if key in ["state"] }
        return await run_tasker_task("MCP Toggle Wifi", filtered_arguments)
    elif name == "tasker_flash_text":
        filtered_arguments = { key: val for key, val in arguments.items() if key in ["text"] }
        return await run_tasker_task("MCP Flash text", filtered_arguments)
    elif name == "tasker_toggle_torch":
        filtered_arguments = { key: val for key, val in arguments.items() if key in ["state"] }
        return await run_tasker_task("MCP Toggle Flashlight", filtered_arguments)
    elif name == "tasker_lamp_on":
        filtered_arguments = { key: val for key, val in arguments.items() if key in [] }
        return await run_tasker_task("MCP Lamp ON", filtered_arguments)
    elif name == "tasker_lamp_off":
        filtered_arguments = { key: val for key, val in arguments.items() if key in [] }
        return await run_tasker_task("MCP Lamp OFF", filtered_arguments)
    elif name == "tasker_get_location":
        filtered_arguments = {}
        return await run_tasker_task("MCP Get Location", filtered_arguments)
    elif name == "tasker_send_sms":
        filtered_arguments = { key: val for key, val in arguments.items() if key in ["number", "message"] }
        return await run_tasker_task("MCP Send SMS", filtered_arguments)
    else:
        return [types.TextContent(type="text", text=f"Error: Unknown tool: {name}")]

async def run_tasker_task(task_name: str, parameters: dict[str, str]) ->  List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Sends an intent to Tasker to run a task."""

    command = [
      "python", "termux-tasker", task_name
    ]

    for key, value in parameters.items():
        command.append(f"--{key}=\"{value}\"")

    logger.info(f"Running command: {' '.join(command)}")

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error_message = f"Error running Tasker task: {stderr.decode()}"
        logger.error(error_message)
        return [types.TextContent(type="text", text=error_message)]

    result_message = f"Tasker task executed successfully.  Output: {stdout.decode()}"
    logger.info(result_message)

    return [types.TextContent(type="text", text=result_message)]

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

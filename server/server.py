import asyncio
import sys
import json
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
    {
        "tasker_name": "MCP Get Battery Level",
        "name": "tasker_get_battery_level",
        "description": "Returns the current battery percentage.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Lamp ON",
        "name": "tasker_lamp_on",
        "description": "Turns the bedroom lamp on.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Lamp OFF",
        "name": "tasker_lamp_off",
        "description": "Turns the bedroom lamp off.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Toggle Flashlight",
        "name": "tasker_toggle_torch",
        "description": "Turns flashlight on or off.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["on", "off"]}
            },
            "required": ["state"]
        }
    },
    {
        "tasker_name": "MCP Flash Text",
        "name": "tasker_flash_text",
        "description": "Displays a short message using tasker Flash action.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to show on the user phone."}
            },
            "required": ["text"]
        }
    },
    {
        "tasker_name": "MCP Say",
        "name": "tasker_tasker_say",
        "description": "Uses Tasker Say action to speak the given text. Use this when asked to 'say', 'recite', 'sing', etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "speech": {"type": "string", "description": "The text to be spoken."},
                "lang": {"type": "string", "description": "The language in the correct Android format (en-usa, spa-usa, etc)."}
            },
            "required": ["speech"]
        }
    },
    {
        "tasker_name": "MCP Send SMS",
        "name": "tasker_send_sms",
        "description": "Sends an SMS message.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "number": {"type": "string", "description": "Recipient phone number."},
                "message": {"type": "string", "description": "Message content."}
            },
            "required": ["number", "message"]
        }
    },
    {
        "tasker_name": "MCP Call Number",
        "name": "tasker_call_number",
        "description": "Initiates a phone call to the specified number.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "number": {"type": "string", "description": "Recipient phone number."},
            },
            "required": ["number"]
        }
    },
    {
        "tasker_name": "MCP Toggle Wifi",
        "name": "tasker_toggle_wifi",
        "description": "Turns WiFi on or off.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "state": {"type": "string", "enum": ["on", "off"]}
            },
            "required": ["state"]
        }
    },
    {
        "tasker_name": "MCP Get Location",
        "name": "tasker_get_location",
        "description": "Retrieves the current GPS coordinates.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Get Contacts",
        "name": "tasker_get_contacts",
        "description": "Retrieves the phone contacts.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP List Files",
        "name": "tasker_list_files",
        "description": "Retrieves the list of files on the phone's Documents folder.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Screenshot",
        "name": "tasker_screenshot",
        "description": "Takes a screenshot of the current screen on the phone.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Browse URL",
        "name": "tasker_browse_url",
        "description": "Opens a URL in the default browser on the phone.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Get Volume",
        "name": "tasker_get_volume",
        "description": "Retrieves the current phone media volume level.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Set Volume",
        "name": "tasker_set_volume",
        "description": "Sets the phone media volume level.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "string",
                    "description": "The media volume level to set (0-15). You understand 'max' as '15', 'min' as '1', and any subjective levels to the corresponding level in a 0 to 15 scale",
                }
            },
            "required": ["level"]
        }
    },
    {
        "tasker_name": "MCP Get Clipboard",
        "name": "tasker_get_clipboard",
        "description": "Retrieves the current phone text clipboard.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Set Clipboard",
        "name": "tasker_set_clipboard",
        "description": "Sets the phone clipboard.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to set the phone clipboard to.",
                }
            },
            "required": ["level"]
        }
    },
    {
        "tasker_name": "MCP Play Music",
        "name": "tasker_play_music",
        "description": "Plays music on the phone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": """The music to search and play on YouTube Music.
Be VERY creative with the query, generating a different one every time, unless explicity asked for a specific song, album or artist.
Otherwise, the same results will show up every time."""
}
            },
            "required": ["query"]
        }
    },
    {
        "tasker_name": "MCP Take Photo",
        "name": "tasker_take_photo",
        "description": "Takes a photo using the phone's camera.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "tasker_name": "MCP Print",
        "name": "tasker_print",
        "description": "Prints a document on the phone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "The path to the document to print"}
            },
            "required": ["path"]
        }
    },
    {
        "tasker_name": "MCP Set Alarm",
        "name": "tasker_set_alarm",
        "description": "Sets an alarm on the phone.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "time": {"type": "string", "description": "Time in 24:00 format"}
            },
            "required": ["text"]
        }
    },
    {
        "tasker_name": "MCP Create Task",
        "name": "tasker_create_google_task",
        "description": "Creates a new task in Google tasks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Task content."}
            },
            "required": ["text"]
        }
    }
]

app = Server(SERVER_NAME)
sse = SseServerTransport("/messages/")

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [types.Tool(**tool) for tool in TOOLS]

#In call tool:
@app.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict
) -> List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    logger.info(f"call_tool: name={name}, arguments={arguments}")

    tool = next((t for t in TOOLS if t['name'] == name), None)

    if tool is not None:
        allowed_arguments = tool['inputSchema']['properties'].keys()
        filtered_arguments = { key: val for key, val in arguments.items() if key in allowed_arguments }

        return await run_tasker_task(tool['tasker_name'], filtered_arguments)
    else:
        return [types.TextContent(type="text", text=f"Error: Unknown tool: {name}")]

async def run_tasker_task(name: str, arguments: dict[str, str]) ->  List[Union[types.TextContent, types.ImageContent, types.EmbeddedResource]]:
    """Sends an intent to Tasker to run a task."""

    data = {
        "name": name,
        "arguments": arguments
    }

    json_data = json.dumps(data)

    command = [
        "curl",
        "-X", "POST",
        "-H", "Content-Type: application/json",
        "-d", json_data,
        "http://0.0.0.0:1821/run_task"
    ]

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

    result_message = f"Tasker task executed successfully."

    if stdout:
        result_message += f" Output: {stdout.decode()}"
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

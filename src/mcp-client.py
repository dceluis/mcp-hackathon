import argparse
import asyncio
import json
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from typing import Optional, Union
from litellm import completion
import traceback

class Client:
    def __init__(self, endpoint, port):
        self.endpoint = endpoint
        self.port = port

        self.session: Optional[ClientSession] = None

        self.tools = {}

    async def call_tool(self, name, arguments):
        async with sse_client(f"{self.endpoint}:{self.port}/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                result = await session.call_tool(name, arguments)

                print(f"Tool call result: {result}")

                return result

    async def initialize(self):
        async with sse_client(f"{self.endpoint}:{self.port}/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                self.session = session

                try:
                    response = await session.list_tools()
                    tools = response.tools
                    print("\nConnected to server with tools:", tools)
                    self.tools = tools

                except Exception as e:
                    print(f"Error calling tool: {e}")

                await write_stream.aclose()


def safe_json_loads(json_obj: Union[str, dict]) -> dict:
    if isinstance(json_obj, dict):
        return json_obj
    else:
        try:
            return json.loads(json_obj)
        except Exception:
            return {}

def to_json_schema(tool) -> dict:
    parameters = tool.inputSchema

    result =  {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
        },
    }
    if not parameters or not parameters['properties']:
        return result

    result["function"]["parameters"] = parameters

    return result

async def main(endpoint, port):
    client = Client(endpoint, port)
    await client.initialize()

    async def chat_loop():
        while True:
            prompt_text = input("> ")
            if prompt_text.lower() in ["exit", "quit"]:
                break
            try:
                tools = [to_json_schema(tool) for tool in client.tools]

                response = await asyncio.to_thread(
                    completion,
                    model="gemini/gemini-2.0-flash-001",
                    messages=[{"role": "user", "content": prompt_text}],
                    tools=tools
                )

                content = response.choices[0].message.content
                tool_calls = response.choices[0].message.tool_calls

                if content:
                    print(content)
                if tool_calls:
                    print(tool_calls)
                    for tool_call in tool_calls:
                        function = tool_call.function
                        name = function.name
                        arguments = safe_json_loads(function.arguments)

                        await client.call_tool(name, arguments)
            except Exception as e:
                print(f"Error during chat completion: {e}")
                traceback.print_exc()

    await chat_loop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MCP client to call tools.')

    parser.add_argument('--endpoint', type=str, default="http://localhost", help='SSE endpoint to connect to')
    parser.add_argument('--port', type=str, default="8000", help='SSE endpoint to connect to')

    args = parser.parse_args()
    asyncio.run(main(args.endpoint, args.port))

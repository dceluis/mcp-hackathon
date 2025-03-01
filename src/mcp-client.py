import argparse
import asyncio
import json
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def main(endpoint, port):
    async with sse_client(f"{endpoint}:{port}/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            try:
                result = await session.call_tool("tasker_toggle_torch", { "state": "on" })
                print(f"Tool call result: {result}")

            except Exception as e:
                print(f"Error calling tool: {e}")

            await write_stream.aclose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MCP client to call tools.')

    parser.add_argument('--endpoint', type=str, default="http://localhost", help='SSE endpoint to connect to')
    parser.add_argument('--port', type=str, default="8000", help='SSE endpoint to connect to')

    args = parser.parse_args()
    asyncio.run(main(args.endpoint, args.port))

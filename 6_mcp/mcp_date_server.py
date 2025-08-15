#!/usr/bin/env python3
"""
MCP Server that provides a tool to get the current date.
This follows the pattern from accounts_server.py in the notebook.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create the MCP server instance
server = Server("date-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """
    List all available tools.
    Returns a tool that can get the current date.
    """
    return [
        Tool(
            name="get_current_date",
            description="Get the current date and time.\n\n    Returns:\n        The current date and time in a human-readable format",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_date_with_format",
            description="Get the current date with a specific format.\n\n    Args:\n        format: The format string (e.g., '%Y-%m-%d', '%B %d, %Y')",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "description": "The datetime format string",
                        "default": "%Y-%m-%d %H:%M:%S"
                    }
                },
                "required": [],
                "additionalProperties": False
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """
    Handle tool calls from the client.
    """
    if name == "get_current_date":
        # Get current date and time
        current_datetime = datetime.now()
        result = f"Current date and time: {current_datetime.strftime('%B %d, %Y at %I:%M %p')}"
        return [TextContent(type="text", text=result)]
    
    elif name == "get_date_with_format":
        # Get the format string from arguments, or use default
        format_string = arguments.get("format", "%Y-%m-%d %H:%M:%S")
        try:
            current_datetime = datetime.now()
            result = current_datetime.strftime(format_string)
            return [TextContent(type="text", text=result)]
        except ValueError as e:
            return [TextContent(type="text", text=f"Error: Invalid format string - {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def main():
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
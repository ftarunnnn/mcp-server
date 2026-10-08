"""
CLI Entry Point for AI Developer MCP Server supporting stdio and SSE transports.
"""

import sys
import click
from ai_developer_mcp.server import mcp, logger


@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport protocol to use: 'stdio' (default) for Claude/Cursor, 'sse' for HTTP streaming."
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host address for SSE transport (default: 0.0.0.0)."
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port for SSE transport (default: 8000)."
)
def main(transport: str, host: str, port: int):
    """
    Launch the AI Developer MCP Server.
    """
    logger.info(f"Starting AI Developer MCP Server via {transport.upper()} transport...")
    
    if transport == "stdio":
        mcp.run(transport="stdio")
    elif transport == "sse":
        # FastMCP SSE runner setup
        logger.info(f"Serving SSE transport on http://{host}:{port}")
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.run(transport="sse")


if __name__ == "__main__":
    main()

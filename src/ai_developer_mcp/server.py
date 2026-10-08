"""
Core MCP server initialization using FastMCP framework.
"""

import sys
import logging
from mcp.server.fastmcp import FastMCP
from ai_developer_mcp.config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("ai_developer_mcp")

# Initialize FastMCP Server
mcp = FastMCP(
    name=config.server_name,
    version=config.server_version,
    description="Enterprise AI Developer Model Context Protocol (MCP) Server"
)

@mcp.tool()
def health_check() -> dict:
    """
    Check the operational status of the MCP server.
    """
    logger.info("Health check tool invoked.")
    return {
        "status": "healthy",
        "server_name": config.server_name,
        "version": config.server_version,
        "workspace_dir": str(config.workspace_dir.absolute())
    }

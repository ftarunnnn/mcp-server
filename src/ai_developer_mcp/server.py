"""
Core MCP server initialization using FastMCP framework.
"""

import sys
import logging
from typing import Any
from mcp.server.fastmcp import FastMCP
from ai_developer_mcp.config import config
import ai_developer_mcp.tools as dev_tools

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

# --- Register Tools ---

@mcp.tool()
def health_check() -> dict:
    """
    Check operational status of the MCP server.
    """
    logger.info("Health check tool invoked.")
    return {
        "status": "healthy",
        "server_name": config.server_name,
        "version": config.server_version,
        "workspace_dir": str(config.workspace_dir.absolute())
    }


@mcp.tool()
def search_code(pattern: str, path: str = ".", max_matches: int = 50) -> dict[str, Any]:
    """
    Search pattern or regex across workspace source files.
    """
    return dev_tools.search_code(pattern=pattern, path=path, max_matches=max_matches)


@mcp.tool()
def analyze_code(code_snippet: str) -> dict[str, Any]:
    """
    Perform AST static code analysis on Python snippet.
    """
    return dev_tools.analyze_code(code_snippet=code_snippet)


@mcp.tool()
def generate_tests(module_name: str, code_snippet: str) -> dict[str, Any]:
    """
    Generate pytest unit test scaffolding for module/snippet.
    """
    return dev_tools.generate_tests(module_name=module_name, code_snippet=code_snippet)


@mcp.tool()
def run_command(command: str, timeout: int = 15) -> dict[str, Any]:
    """
    Execute controlled terminal command within workspace (git, pytest, python, pip, etc.).
    """
    return dev_tools.run_command(command=command, timeout=timeout)


@mcp.tool()
def search_documentation(query: str) -> dict[str, Any]:
    """
    Search documentation and docstrings in project.
    """
    return dev_tools.search_documentation(query=query)


@mcp.tool()
def git_operations(action: str, target: str = "") -> dict[str, Any]:
    """
    Execute safe git queries (status, log, diff, branch).
    """
    return dev_tools.git_operations(action=action, target=target)

"""
Core MCP server initialization using FastMCP framework.
"""

import sys
import logging
from typing import Any
from mcp.server.fastmcp import FastMCP
from ai_developer_mcp.config import config
import ai_developer_mcp.tools as dev_tools
import ai_developer_mcp.resources as dev_resources
import ai_developer_mcp.prompts as dev_prompts
import ai_developer_mcp.services as dev_services

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


@mcp.tool()
async def github_get_repo_info(owner: str, repo: str) -> dict[str, Any]:
    """
    Fetch live repository metadata and stargazers count from GitHub REST API.
    """
    return await dev_services.github_get_repo_info(owner=owner, repo=repo)


@mcp.tool()
async def github_search_issues(query: str, owner: str = "", repo: str = "") -> dict[str, Any]:
    """
    Search GitHub issues and pull requests for given topic/query.
    """
    return await dev_services.github_search_issues(query=query, owner=owner, repo=repo)


# --- Register Resources ---

@mcp.resource("project://files/{path}")
def project_file_resource(path: str) -> str:
    """
    Dynamic resource accessing project workspace file content.
    """
    return dev_resources.get_project_file(path)


@mcp.resource("docs://architecture")
def architecture_docs_resource() -> str:
    """
    Static resource exposing system architecture documentation.
    """
    return dev_resources.get_architecture_docs()


@mcp.resource("config://server-status")
def server_status_resource() -> str:
    """
    Static resource exposing MCP server runtime configuration and health status.
    """
    return dev_resources.get_server_config_status()


# --- Register Prompts ---

@mcp.prompt()
def code_review(code_snippet: str, language: str = "python", strictness: str = "normal") -> str:
    """
    Reusable prompt workflow for automated code review.
    """
    return dev_prompts.prompt_code_review(code_snippet=code_snippet, language=language, strictness=strictness)


@mcp.prompt()
def debugging(error_message: str, stack_trace: str, code_context: str = "") -> str:
    """
    Reusable prompt workflow for root-cause error debugging.
    """
    return dev_prompts.prompt_debugging(error_message=error_message, stack_trace=stack_trace, code_context=code_context)


@mcp.prompt()
def architecture_review(system_description: str, tech_stack: str = "") -> str:
    """
    Reusable prompt workflow for software architecture evaluation.
    """
    return dev_prompts.prompt_architecture_review(system_description=system_description, tech_stack=tech_stack)

"""
Resource definitions for exposing dynamic project files, documentation, and configuration.
"""

import json
from pathlib import Path
from ai_developer_mcp.config import config


def get_project_file(path: str) -> str:
    """
    Read and return file content from workspace root.
    URI format: project://files/{path}
    """
    file_path = config.workspace_dir / path
    if not file_path.exists():
        return f"Error: File '{path}' not found in workspace."
    if file_path.is_dir():
        return f"Error: Path '{path}' is a directory."

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file '{path}': {str(e)}"


def get_architecture_docs() -> str:
    """
    Return system architecture documentation.
    URI format: docs://architecture
    """
    arch_file = config.workspace_dir / "docs" / "phases" / "01-mcp-fundamentals.md"
    if arch_file.exists():
        return arch_file.read_text(encoding="utf-8")
    return "AI Developer MCP Server Architecture: FastMCP + SQLite + Stdio/SSE."


def get_server_config_status() -> str:
    """
    Return server configuration and runtime status as formatted JSON.
    URI format: config://server-status
    """
    status_data = {
        "server_name": config.server_name,
        "version": config.server_version,
        "workspace_dir": str(config.workspace_dir.absolute()),
        "log_level": config.log_level,
        "api_key_enabled": config.required_api_key is not None,
        "github_integration": config.github_token is not None
    }
    return json.dumps(status_data, indent=2)

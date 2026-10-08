"""
MCP Resources module.
"""

from ai_developer_mcp.resources.project_resources import (
    get_project_file,
    get_architecture_docs,
    get_server_config_status
)

__all__ = [
    "get_project_file",
    "get_architecture_docs",
    "get_server_config_status"
]

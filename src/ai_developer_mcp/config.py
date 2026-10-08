"""
Configuration management for AI Developer MCP Server.
"""

import os
from pathlib import Path
from pydantic import BaseModel


class Config(BaseModel):
    server_name: str = "AI Developer MCP Server"
    server_version: str = "1.0.0"
    workspace_dir: Path = Path(os.getenv("MCP_WORKSPACE_DIR", os.getcwd()))
    db_path: Path = Path(os.getenv("MCP_DB_PATH", "mcp_server.db"))
    api_key_header: str = "X-MCP-API-Key"
    required_api_key: str | None = os.getenv("MCP_API_KEY", None)
    log_level: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    github_token: str | None = os.getenv("GITHUB_TOKEN", None)


config = Config()

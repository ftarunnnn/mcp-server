# Phase 2: Environment Setup & Configuration

## 1. Project Directory Structure

```
mcp-server/
├── docs/
│   └── phases/
│       ├── 01-mcp-fundamentals.md
│       └── 02-environment-setup.md
├── src/
│   └── ai_developer_mcp/
│       ├── __init__.py
│       ├── config.py
│       ├── server.py
│       ├── main.py
│       ├── tools/
│       ├── resources/
│       ├── prompts/
│       ├── services/
│       ├── db/
│       └── auth/
├── tests/
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## 2. Dependencies & Framework Selection

- **Python 3.10+**: Offers async native capabilities, union typing (`str | None`), and fast execution.
- **FastMCP (Official MCP Python SDK)**: High-level Python server framework with decorator-based tool/resource/prompt registration and automatic JSON Schema generation.
- **Pydantic v2**: Type validation and schema definition for tools.
- **HTTPX**: Async HTTP client for external API integrations (GitHub API, DevDocs).
- **SQLite3**: Zero-config persistent database for audit logging and permissions.

## 3. Environment Variables Configuration

- `MCP_WORKSPACE_DIR`: Base directory for filesystem and git operations (default: current working directory).
- `MCP_DB_PATH`: Path to SQLite database file (default: `mcp_server.db`).
- `MCP_API_KEY`: API Key for server authorization (optional).
- `GITHUB_TOKEN`: Personal access token for GitHub API integration (optional).

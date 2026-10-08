# Phase 3: Basic MCP Server Initialization

## 1. Overview

In Phase 3, we initialize the core FastMCP server instance, configure metadata, add a standard health check tool, and expose a CLI entry point for dual-transport execution (`stdio` and `sse`).

## 2. Code Architecture

- **`src/ai_developer_mcp/server.py`**:
  - Instantiates `FastMCP("AI Developer MCP Server", version="1.0.0")`.
  - Registers basic `health_check()` tool returning server status, version, and current workspace directory.
  - Sets up structured stderr logging.

- **`src/ai_developer_mcp/main.py`**:
  - Command-line interface with options `--transport [stdio|sse]`, `--host`, and `--port`.
  - Stdio transport communicates via standard input/output streams for AI desktop integration.
  - SSE transport runs an HTTP server for remote/web AI clients.

## 3. Running the Server

### Stdio Transport (Default)
```bash
python -m ai_developer_mcp.main --transport stdio
```

### SSE Transport (HTTP Server)
```bash
python -m ai_developer_mcp.main --transport sse --port 8000
```

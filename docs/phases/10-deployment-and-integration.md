# Phase 10: Deployment & AI Client Integration

## 1. Overview

Phase 10 provides configuration files and container deployment manifests to integrate the AI Developer MCP Server into Claude Desktop, Cursor IDE, Docker container environments, and cloud infrastructure.

## 2. Integrating with Claude Desktop

1. Open your Claude Desktop configuration file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the server entry from `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ai-developer": {
      "command": "python",
      "args": [
        "-m",
        "ai_developer_mcp.main",
        "--transport",
        "stdio"
      ],
      "env": {
        "MCP_WORKSPACE_DIR": "/path/to/your/project",
        "MCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```
3. Restart Claude Desktop. The hammer icon will show 9 tools, 3 resources, and 3 prompts ready for use.

## 3. Container Deployment (Docker & docker-compose)

### Build and Run with Docker
```bash
docker build -t ai-developer-mcp .
docker run -d -p 8000:8000 -v $(pwd):/app ai-developer-mcp
```

### Run with docker-compose
```bash
docker-compose up -d
```
The SSE endpoint will be live at `http://localhost:8000/sse`.

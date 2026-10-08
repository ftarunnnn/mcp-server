# Phase 5: Expose Structured Resources

## 1. Overview

MCP Resources allow AI clients to dynamically read context data (files, system state, docs) using standardized URI templates (`scheme://path`).

## 2. Resource Inventory

| URI Scheme / Template | Type | Description |
| :--- | :--- | :--- |
| `project://files/{path}` | Dynamic Template | Exposes file content relative to workspace directory. |
| `docs://architecture` | Static Resource | Exposes system architecture documentation. |
| `config://server-status` | Static Resource | Exposes JSON formatted runtime configuration and status. |

## 3. Client Interaction Example

An AI client can request:
```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "resources/read",
  "params": {
    "uri": "project://files/pyproject.toml"
  }
}
```
The server responds with the contents of `pyproject.toml` safely isolated inside the workspace directory.

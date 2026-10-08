# Phase 1: Model Context Protocol (MCP) Fundamentals

## 1. Overview of MCP Architecture

The **Model Context Protocol (MCP)** is an open specification created by Anthropic that standardizes how Artificial Intelligence applications (clients) securely connect to data sources, tools, and developer resources (servers).

Prior to MCP, every AI tool integration required custom glue code, ad-hoc API wrappers, and complex prompt engineering. MCP establishes a universal binary/JSON protocol allowing AI models to dynamically inspect server capabilities, call tools with typed parameters, read dynamic resources, and execute standardized prompts.

```mermaid
flowchart LR
    subgraph AI Client Layer
        Claude["Claude Desktop"]
        Cursor["Cursor / VS Code"]
        CustomAgent["Custom AI Agent"]
    end

    subgraph Transport Layer
        Stdio["Stdio (JSON-RPC)"]
        SSE["SSE / HTTP (Server-Sent Events)"]
    end

    subgraph MCP Server ["AI Developer MCP Server"]
        Metadata["Server Metadata & Capabilities"]
        
        subgraph Core Features
            Tools["Tools (search, analyze, git, commands)"]
            Resources["Resources (project files, docs, status)"]
            Prompts["Prompts (code review, debugging, arch)"]
        end

        subgraph Storage & Auth
            DB["SQLite Audit Log & Storage"]
            Auth["API Key Auth & RBAC"]
        end
    end

    AI Client Layer <--> Transport Layer
    Transport Layer <--> MCP Server
```

---

## 2. Core Concepts: Tools, Resources & Prompts

| Concept | Description | Example in AI Developer MCP Server |
| :--- | :--- | :--- |
| **Tools** | Executable functions called by the AI to mutate state or execute logic. | `search_code()`, `analyze_code()`, `git_operations()`, `run_command()` |
| **Resources** | Read-only context data exposed to the AI via URI schemes. | `project://files/{path}`, `docs://architecture`, `config://server-status` |
| **Prompts** | Parameterized prompt templates that standardize AI workflows. | `code_review`, `debugging`, `architecture_review` |

---

## 3. Protocol Transports & Message Format

MCP supports two primary transport mechanisms:

1. **Stdio (Standard Input / Output)**:
   - Primary transport for desktop AI clients (Claude Desktop, Cursor).
   - High security, zero network exposure, subprocess communication via JSON-RPC 2.0.

2. **SSE (Server-Sent Events over HTTP)**:
   - Ideal for remote services, multi-tenant deployments, and web interfaces.
   - Client sends commands via HTTP POST, server streams responses via HTTP SSE.

### JSON-RPC 2.0 Message Lifecycle Example

#### Tool List Request (`tools/list`)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

#### Server Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "search_code",
        "description": "Search code by regex pattern across workspace files",
        "inputSchema": {
          "type": "object",
          "properties": {
            "pattern": { "type": "string" },
            "path": { "type": "string", "default": "." }
          },
          "required": ["pattern"]
        }
      }
    ]
  }
}
```

#### Tool Call Request (`tools/call`)
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_code",
    "arguments": {
      "pattern": "def main",
      "path": "src"
    }
  }
}
```

---

## 4. Key Security Principles in MCP

1. **Explicit Consent & Granular Permissions**: Tools that execute commands (`run_command`) require user authorization or allowlist validation.
2. **Context Isolation**: Resources are bounded to allowed filesystem roots or database tables.
3. **Audit Trail**: Every tool invocation and resource read is logged into SQLite for compliance and debugging.

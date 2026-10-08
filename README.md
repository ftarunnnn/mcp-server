# AI Developer MCP Server 🚀

An enterprise-grade, production-ready **Model Context Protocol (MCP)** server built from scratch in Python using **FastMCP**.

This server equips AI assistants (Claude Desktop, Cursor, Custom LLM Agents) with powerful software engineering tools, structured project resources, reusable prompt templates, SQLite persistence, API authentication, and containerized deployment options.

---

## 🏗️ Project Architecture & 10-Phase Blueprint

| Phase | Phase Name | Description | Key Deliverable |
| :---: | :--- | :--- | :--- |
| **Phase 1** | **MCP Fundamentals** | Architecture, JSON-RPC, transport layer, core primitives | [`docs/phases/01-mcp-fundamentals.md`](docs/phases/01-mcp-fundamentals.md) |
| **Phase 2** | **Environment Setup** | FastMCP setup, dependencies, structure, config | `pyproject.toml`, project layout |
| **Phase 3** | **Basic MCP Server** | Server initialization, stdio & SSE transports | `src/ai_developer_mcp/server.py` |
| **Phase 4** | **Build Tools** | Search code, AST analysis, test gen, commands, git | `src/ai_developer_mcp/tools/` |
| **Phase 5** | **Resources** | Dynamic file resources, docs, config URIs | `src/ai_developer_mcp/resources/` |
| **Phase 6** | **Prompts** | Reusable code review, debugging, arch workflows | `src/ai_developer_mcp/prompts/` |
| **Phase 7** | **External API Integration** | GitHub REST API, issue search, dev docs search | `src/ai_developer_mcp/services/` |
| **Phase 8** | **Database & Auth** | SQLite audit logging, API key middleware, RBAC | `src/ai_developer_mcp/db/` |
| **Phase 9** | **Testing & Error Handling**| Pytest unit/integration suite, structured logs | `tests/` & error handling |
| **Phase 10**| **Deployment & Integration** | Claude Desktop config, Docker, multi-platform setup | `Dockerfile`, `docker-compose.yml` |

---

## 🛠️ System Overview

```
AI Developer MCP Server
│
├── Tools (Capabilities)
│   ├── search_code()       -> Fast regex code search across workspace
│   ├── analyze_code()      -> AST syntax parsing, metrics, complexity
│   ├── generate_tests()     -> Automated unit test template generation
│   ├── run_command()       -> Controlled terminal command execution
│   ├── search_documentation() -> Local markdown & docstring lookup
│   ├── git_operations()    -> Git status, diff, commit log, branch inspection
│   └── github_get_repo_info() -> Live GitHub API integration
│
├── Resources (Context Data)
│   ├── project://files/{path} -> Dynamic project file accessor
│   ├── docs://architecture    -> System architecture reference
│   └── config://server-status -> Live server health & status
│
└── Prompts (Workflows)
    ├── code_review          -> Comprehensive security & quality review
    ├── debugging            -> Stack trace root-cause analyzer
    └── architecture_review  -> Software architecture evaluation
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/ftarunnnn/mcp-server.git
cd mcp-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Running the Server

#### Stdio Mode (Default for Claude Desktop / Cursor)
```bash
python -m ai_developer_mcp.main
```

#### SSE Mode (HTTP Server on Port 8000)
```bash
python -m ai_developer_mcp.main --transport sse --port 8000
```

---

## 📄 License
MIT License - created for learning and production MCP deployment.
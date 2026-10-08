# Phase 8: Database + Authentication

## 1. Overview

Phase 8 equips the MCP server with enterprise database persistence (SQLite) for audit logging and API key-based authentication with Role-Based Access Control (RBAC).

## 2. Database Schema

- **`audit_logs` Table**:
  - `id`: INTEGER PRIMARY KEY AUTOINCREMENT
  - `timestamp`: REAL (epoch seconds)
  - `event_type`: TEXT ('TOOL', 'RESOURCE', 'PROMPT', 'AUTH')
  - `name`: TEXT (e.g. 'run_command', 'project_file_resource')
  - `caller`: TEXT (client ID / anonymous)
  - `status`: TEXT ('SUCCESS', 'FAILURE')
  - `details`: TEXT (JSON summary or error message)

- **`api_keys` Table**:
  - `id`: INTEGER PRIMARY KEY
  - `key_hash`: TEXT UNIQUE
  - `client_name`: TEXT
  - `role`: TEXT ('admin', 'developer', 'readonly')
  - `created_at`: REAL
  - `is_active`: INTEGER (1 or 0)

## 3. RBAC Roles & Permissions

| Role | Permissions |
| :--- | :--- |
| `admin` | Full access to all tools (including system commands), resources, and prompts. |
| `developer` | Access to developer tools (`search_code`, `analyze_code`, `git_operations`), resources, and prompts. |
| `readonly` | Access to resources and read-only search tools (`search_documentation`). |

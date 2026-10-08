# Phase 4: Build Developer Tools

## 1. Overview

Phase 4 implements 6 essential tools for software development workflows, exposing them through `@mcp.tool()` decorators with strict input and output typing.

## 2. Tool Inventory

| Tool Name | Input Parameters | Description |
| :--- | :--- | :--- |
| `search_code` | `pattern: str`, `path: str`, `max_matches: int` | Searches regex patterns across workspace files with line numbers and file paths. |
| `analyze_code` | `code_snippet: str` | AST-based Python code analysis for syntax errors, function/class metrics, loc, and imports. |
| `generate_tests` | `module_name: str`, `code_snippet: str` | Generates runnable `pytest` test scaffolding for functions in snippet. |
| `run_command` | `command: str`, `timeout: int` | Secure subprocess runner with command allowlisting (`git`, `pytest`, `python`, `pip`). |
| `search_documentation`| `query: str` | Searches markdown documentation and docstrings in `docs/` folder. |
| `git_operations` | `action: str`, `target: str` | Executes git `status`, `log`, `diff`, and `branch` commands safely. |

## 3. Schema & Validation

FastMCP automatically extracts Pydantic/type-hint schemas for each tool and exposes them via `tools/list` to AI clients.

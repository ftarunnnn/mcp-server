# Phase 6: Standardized Reusable Prompts

## 1. Overview

MCP Prompts provide parameterized prompt templates for standardizing developer workflows (code review, debugging, architectural design) across different AI tools and clients.

## 2. Prompt Inventory

| Prompt Name | Parameters | Purpose |
| :--- | :--- | :--- |
| `code_review` | `code_snippet: str`, `language: str`, `strictness: str` | Standardized prompt for code quality, security, and refactoring review. |
| `debugging` | `error_message: str`, `stack_trace: str`, `code_context: str` | Standardized root-cause analysis prompt for stack traces. |
| `architecture_review` | `system_description: str`, `tech_stack: str` | Standardized architecture evaluation and blueprint assessment prompt. |

## 3. Invocation Protocol Example

Clients fetch prompt definitions via `prompts/list` and request prompt generation via `prompts/get`:
```json
{
  "jsonrpc": "2.0",
  "id": 15,
  "method": "prompts/get",
  "params": {
    "name": "code_review",
    "arguments": {
      "code_snippet": "def add(a, b): return a + b",
      "language": "python"
    }
  }
}
```

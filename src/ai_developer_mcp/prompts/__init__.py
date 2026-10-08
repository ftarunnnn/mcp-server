"""
MCP Prompts module.
"""

from ai_developer_mcp.prompts.dev_prompts import (
    prompt_code_review,
    prompt_debugging,
    prompt_architecture_review
)

__all__ = [
    "prompt_code_review",
    "prompt_debugging",
    "prompt_architecture_review"
]

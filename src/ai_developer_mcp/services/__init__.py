"""
External API services module.
"""

from ai_developer_mcp.services.github_service import (
    github_get_repo_info,
    github_search_issues
)

__all__ = [
    "github_get_repo_info",
    "github_search_issues"
]

"""
External GitHub REST API service integration using HTTPX.
"""

from typing import Any
import httpx
from ai_developer_mcp.config import config


async def github_get_repo_info(owner: str, repo: str) -> dict[str, Any]:
    """
    Fetch repository metadata and status from GitHub API.
    
    :param owner: Repository owner username or organization.
    :param repo: Repository name.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Developer-MCP-Server"
    }
    if config.github_token:
        headers["Authorization"] = f"token {config.github_token}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                return {
                    "full_name": data.get("full_name"),
                    "description": data.get("description"),
                    "stars": data.get("stargazers_count"),
                    "forks": data.get("forks_count"),
                    "open_issues": data.get("open_issues_count"),
                    "language": data.get("language"),
                    "html_url": data.get("html_url")
                }
            return {
                "error": f"GitHub API returned status {response.status_code}",
                "detail": response.text
            }
        except Exception as e:
            return {"error": f"HTTP request failed: {str(e)}"}


async def github_search_issues(query: str, owner: str = "", repo: str = "") -> dict[str, Any]:
    """
    Search GitHub issues and pull requests for given query.
    
    :param query: Search query term.
    :param owner: Optional repo owner filter.
    :param repo: Optional repo name filter.
    """
    search_q = query
    if owner and repo:
        search_q += f" repo:{owner}/{repo}"

    url = f"https://api.github.com/search/issues?q={search_q}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Developer-MCP-Server"
    }
    if config.github_token:
        headers["Authorization"] = f"token {config.github_token}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            if response.status_code == 200:
                data = response.json()
                items = []
                for item in data.get("items", [])[:10]:
                    items.append({
                        "title": item.get("title"),
                        "number": item.get("number"),
                        "state": item.get("state"),
                        "html_url": item.get("html_url"),
                        "created_at": item.get("created_at")
                    })
                return {
                    "total_count": data.get("total_count"),
                    "items": items
                }
            return {"error": f"GitHub API error {response.status_code}", "detail": response.text}
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

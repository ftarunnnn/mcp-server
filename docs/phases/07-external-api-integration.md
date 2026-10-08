# Phase 7: External API Integration

## 1. Overview

In Phase 7, we integrate external REST services directly into the MCP server using async HTTP requests (`httpx`). This transforms the server from a local file-only tool into a connected developer platform.

## 2. GitHub REST API Integration

- **`github_get_repo_info`**: Fetches repository metadata, star count, forks, language, open issues, and HTML links from `https://api.github.com/repos/{owner}/{repo}`.
- **`github_search_issues`**: Searches GitHub issues and pull requests by keyword or repo target.

## 3. Configuration & Rate Limits

- Supports `GITHUB_TOKEN` environment variable for authenticated requests (up to 5,000 requests/hour vs 60 requests/hour unauthenticated).
- Uses non-blocking async HTTP clients with automatic timeout management.

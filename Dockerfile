# Production Dockerfile for AI Developer MCP Server
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY pyproject.toml requirements.txt README.md ./
COPY src/ ./src/

# Install python dependencies and package
RUN pip install --no-cache-dir .

# Expose port for SSE transport
EXPOSE 8000

# Set default workspace directory
ENV MCP_WORKSPACE_DIR=/app
ENV MCP_LOG_LEVEL=INFO

# Default entry point (runs SSE mode in Docker container)
CMD ["python", "-m", "ai_developer_mcp.main", "--transport", "sse", "--host", "0.0.0.0", "--port", "8000"]

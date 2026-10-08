"""
Unit tests for resources and prompts.
"""

from ai_developer_mcp.resources import (
    get_project_file,
    get_architecture_docs,
    get_server_config_status
)
from ai_developer_mcp.prompts import (
    prompt_code_review,
    prompt_debugging,
    prompt_architecture_review
)


def test_resources():
    file_content = get_project_file("pyproject.toml")
    assert "ai-developer-mcp" in file_content

    arch = get_architecture_docs()
    assert "MCP" in arch

    config_status = get_server_config_status()
    assert "server_name" in config_status


def test_prompts():
    cr = prompt_code_review("print('hello')", language="python")
    assert "Senior Principal Software Engineer" in cr
    assert "print('hello')" in cr

    dbg = prompt_debugging("NullPointer", "Traceback line 10")
    assert "NullPointer" in dbg

    arch_rev = prompt_architecture_review("Microservices with Kafka")
    assert "Microservices with Kafka" in arch_rev

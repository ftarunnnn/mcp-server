"""
Unit tests for core developer tools.
"""

from ai_developer_mcp.tools import (
    search_code,
    analyze_code,
    generate_tests,
    run_command,
    git_operations
)


def test_analyze_code_valid():
    snippet = """
def add(a: int, b: int) -> int:
    \"\"\"Add two numbers.\"\"\"
    return a + b
"""
    res = analyze_code(snippet)
    assert res["valid"] is True
    assert res["metrics"]["function_count"] == 1
    assert res["functions"][0]["name"] == "add"


def test_analyze_code_invalid_syntax():
    snippet = "def broken_func("
    res = analyze_code(snippet)
    assert res["valid"] is False
    assert "Syntax error" in res["error"]


def test_generate_tests():
    snippet = "def calculate_total(price, tax):\n    return price + tax"
    res = generate_tests("billing", snippet)
    assert res["module"] == "billing"
    assert "def test_calculate_total_basic" in res["generated_test_code"]


def test_run_command_allowed():
    res = run_command("git --version")
    assert res["success"] is True
    assert "git version" in res["stdout"].lower()


def test_run_command_disallowed():
    res = run_command("rm -rf /")
    assert res["success"] is False
    assert "not in allowed list" in res["error"]


def test_search_code():
    res = search_code("def ", path="src")
    assert res["total"] > 0
    assert len(res["matches"]) > 0


def test_git_operations():
    res = git_operations("status")
    assert res["success"] is True
    assert "branch" in res["stdout"].lower() or "on branch" in res["stdout"].lower()

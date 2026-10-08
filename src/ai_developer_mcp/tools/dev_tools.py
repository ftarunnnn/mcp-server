"""
Developer tools implementation for AI Developer MCP Server.
"""

import ast
import os
import re
import subprocess
from pathlib import Path
from typing import Any
from ai_developer_mcp.config import config


def search_code(pattern: str, path: str = ".", max_matches: int = 50) -> dict[str, Any]:
    """
    Search for regex pattern across files in workspace.
    
    :param pattern: Regular expression string to search for.
    :param path: Subdirectory path relative to workspace root.
    :param max_matches: Maximum number of matches to return.
    """
    target_dir = config.workspace_dir / path
    if not target_dir.exists():
        return {"error": f"Path '{path}' does not exist."}

    compiled = re.compile(pattern)
    results = []

    for root, _, files in os.walk(target_dir):
        # Ignore git and venv directories
        if ".git" in root or ".venv" in root or "__pycache__" in root:
            continue
        for file in files:
            file_path = Path(root) / file
            # Only search text files
            if file_path.suffix not in [".py", ".ts", ".js", ".json", ".md", ".toml", ".txt", ".yml", ".html", ".css"]:
                continue
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        if compiled.search(line):
                            rel_path = file_path.relative_to(config.workspace_dir)
                            results.append({
                                "file": str(rel_path),
                                "line_number": line_num,
                                "content": line.strip()
                            })
                            if len(results) >= max_matches:
                                return {"matches": results, "total": len(results), "truncated": True}
            except Exception as e:
                continue

    return {"matches": results, "total": len(results), "truncated": False}


def analyze_code(code_snippet: str) -> dict[str, Any]:
    """
    Perform AST analysis on Python code snippet.
    
    :param code_snippet: Source code text to analyze.
    """
    try:
        parsed = ast.parse(code_snippet)
    except SyntaxError as se:
        return {
            "valid": False,
            "error": f"Syntax error at line {se.lineno}, col {se.offset}: {se.msg}"
        }

    functions = []
    classes = []
    imports = []

    for node in ast.walk(parsed):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node)
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "line": node.lineno,
                "docstring": ast.get_docstring(node)
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module if node.module else "")

    lines = code_snippet.splitlines()

    return {
        "valid": True,
        "metrics": {
            "total_lines": len(lines),
            "loc": len([l for l in lines if l.strip() and not l.strip().startswith("#")]),
            "function_count": len(functions),
            "class_count": len(classes),
            "import_count": len(imports)
        },
        "functions": functions,
        "classes": classes,
        "imports": list(set(imports))
    }


def generate_tests(module_name: str, code_snippet: str) -> dict[str, Any]:
    """
    Generate pytest template for code functions or module.
    
    :param module_name: Target module name.
    :param code_snippet: Source code snippet.
    """
    analysis = analyze_code(code_snippet)
    if not analysis.get("valid"):
        return {"error": "Invalid Python code snippet cannot generate tests."}

    test_cases = []
    for func in analysis.get("functions", []):
        func_name = func["name"]
        args = ", ".join(func["args"])
        test_cases.append(f"""
def test_{func_name}_basic():
    # TODO: Supply valid arguments for {func_name}({args})
    # result = {func_name}(...)
    # assert result is not None
    pass
""")

    test_file_content = f"""# Auto-generated unit tests for {module_name}
import pytest

{ "".join(test_cases) }
"""
    return {
        "module": module_name,
        "generated_test_code": test_file_content.strip(),
        "function_count": len(analysis.get("functions", []))
    }


def run_command(command: str, timeout: int = 15) -> dict[str, Any]:
    """
    Execute controlled terminal command within workspace directory.
    
    :param command: Command string to execute.
    :param timeout: Maximum execution time in seconds.
    """
    # Allowed command prefixes for security
    allowed_prefixes = ["git", "pytest", "python", "pip", "dir", "ls", "echo", "node"]
    cmd_parts = command.strip().split()
    if not cmd_parts or cmd_parts[0].lower() not in allowed_prefixes:
        return {
            "success": False,
            "error": f"Command '{cmd_parts[0] if cmd_parts else ''}' is not in allowed list: {allowed_prefixes}"
        }

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=config.workspace_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout} seconds."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def search_documentation(query: str) -> dict[str, Any]:
    """
    Search for documentation matches in project markdown files and docstrings.
    
    :param query: Search query term.
    """
    matches = search_code(re.escape(query), path="docs")
    return {
        "query": query,
        "results": matches.get("matches", []),
        "count": matches.get("total", 0)
    }


def git_operations(action: str, target: str = "") -> dict[str, Any]:
    """
    Perform safe git operations: status, log, diff, branch.
    
    :param action: Git action ('status', 'log', 'diff', 'branch').
    :param target: Optional target parameter (e.g. branch name or file).
    """
    actions = {
        "status": "git status",
        "log": f"git log -n 5 {target}".strip(),
        "diff": f"git diff {target}".strip(),
        "branch": "git branch -a"
    }

    if action not in actions:
        return {"error": f"Action '{action}' unsupported. Valid actions: {list(actions.keys())}"}

    cmd = actions[action]
    return run_command(cmd)

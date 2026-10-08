"""
MCP Prompts for standardized AI developer workflows.
"""


def prompt_code_review(code_snippet: str, language: str = "python", strictness: str = "normal") -> str:
    """
    Generate automated code review prompt.
    """
    return f"""You are a Senior Principal Software Engineer performing a rigorous code review.

Target Language: {language}
Review Strictness: {strictness}

Please analyze the following code snippet and provide:
1. Executive Summary & Quality Score (1-10)
2. Security Vulnerabilities & Edge Cases
3. Performance & Algorithmic Optimizations
4. Readability, Refactoring, & Best Practices
5. Refactored Code Suggestion

Code Snippet:
```{language}
{code_snippet}
```
"""


def prompt_debugging(error_message: str, stack_trace: str, code_context: str = "") -> str:
    """
    Generate root cause debugging prompt.
    """
    return f"""You are an Expert Debugging Assistant. Help diagnose and resolve this issue.

Error Message:
{error_message}

Stack Trace:
```
{stack_trace}
```

Code Context:
```
{code_context if code_context else "No extra code context provided."}
```

Please perform root cause analysis and provide:
1. Primary Root Cause Explanation
2. Immediate Fix Code Diff / Snippet
3. Prevention Strategies & Test Case Recommendations
"""


def prompt_architecture_review(system_description: str, tech_stack: str = "") -> str:
    """
    Generate software architecture evaluation prompt.
    """
    return f"""You are an Enterprise Systems Architect. Evaluate the following software architecture proposal.

Technology Stack:
{tech_stack if tech_stack else "Not specified"}

System Architecture Description:
{system_description}

Please provide an Architectural Assessment covering:
1. Architectural Style & Component Decoupling
2. Scalability, Latency & Throughput Bottlenecks
3. Resilience, High Availability & Failover Strategy
4. Security Boundary & Auth/Access Model
5. Key Recommendations & Diagrammatic Blueprint
"""

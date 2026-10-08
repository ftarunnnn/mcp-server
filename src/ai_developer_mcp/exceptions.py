"""
Custom exception classes and error handling for AI Developer MCP Server.
"""


class MCPBaseException(Exception):
    """Base exception class for MCP server errors."""
    def __init__(self, message: str, code: int = -32603):
        super().__init__(message)
        self.message = message
        self.code = code


class MCPToolError(MCPBaseException):
    """Raised when a tool execution fails."""
    def __init__(self, message: str):
        super().__init__(message, code=-32000)


class AuthenticationError(MCPBaseException):
    """Raised when authentication fails."""
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, code=-32001)


class SecurityViolationError(MCPBaseException):
    """Raised when a command violates security allowlist rules."""
    def __init__(self, command: str):
        super().__init__(f"Command '{command}' violates security policy", code=-32002)

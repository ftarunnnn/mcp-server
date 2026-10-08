"""
Authentication and Role-Based Access Control (RBAC) middleware logic.
"""

from typing import Any
from ai_developer_mcp.config import config
from ai_developer_mcp.db import verify_api_key, log_audit_event


class SecurityContext:
    @staticmethod
    def authenticate(api_key: str | None) -> dict[str, Any]:
        """
        Validate incoming request credentials against config and SQLite database.
        """
        if not config.required_api_key:
            return {"authenticated": True, "client_name": "anonymous", "role": "admin"}

        if not api_key:
            log_audit_event("AUTH", "authenticate", "FAILURE", "anonymous", "Missing API key")
            return {"authenticated": False, "error": "Missing API key"}

        if api_key == config.required_api_key:
            return {"authenticated": True, "client_name": "master_admin", "role": "admin"}

        db_user = verify_api_key(api_key)
        if db_user:
            return {"authenticated": True, "client_name": db_user["client_name"], "role": db_user["role"]}

        log_audit_event("AUTH", "authenticate", "FAILURE", "invalid_key", "Invalid API key provided")
        return {"authenticated": False, "error": "Invalid API Key"}

    @staticmethod
    def check_permission(role: str, action_type: str) -> bool:
        """
        Check if role has permission to execute given action.
        """
        if role == "admin":
            return True
        if role == "developer" and action_type != "admin_only":
            return True
        if role == "readonly" and action_type in ["read_tool", "resource"]:
            return True
        return False

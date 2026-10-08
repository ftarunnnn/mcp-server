"""
Unit tests for database and security context.
"""

import os
from ai_developer_mcp.config import config
from ai_developer_mcp.db import (
    init_db,
    log_audit_event,
    register_api_key,
    verify_api_key
)
from ai_developer_mcp.auth import SecurityContext


def test_db_and_auth():
    # Remove existing db if present for test cleanliness
    if config.db_path.exists():
        try:
            os.remove(config.db_path)
        except PermissionError:
            pass

    init_db()
    log_audit_event("TEST", "test_event", "SUCCESS", "pytest", "unit test run")

    success = register_api_key("test_key_unique_999", "test_client", role="developer")
    assert success is True

    record = verify_api_key("test_key_unique_999")
    assert record is not None
    assert record["client_name"] == "test_client"
    assert record["role"] == "developer"

    auth_res = SecurityContext.authenticate("test_key_unique_999")
    assert auth_res["authenticated"] is True
    assert auth_res["client_name"] == "test_client"

    assert SecurityContext.check_permission("admin", "any") is True
    assert SecurityContext.check_permission("readonly", "read_tool") is True
    assert SecurityContext.check_permission("readonly", "admin_only") is False

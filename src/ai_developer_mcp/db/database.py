"""
SQLite Database persistence layer for audit logging and API key management.
"""

import sqlite3
import time
from typing import Any
from ai_developer_mcp.config import config


def get_db_connection() -> sqlite3.Connection:
    """
    Establish connection to SQLite database.
    """
    conn = sqlite3.connect(config.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Initialize database tables for audit logging and API keys.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                event_type TEXT NOT NULL,
                name TEXT NOT NULL,
                caller TEXT,
                status TEXT NOT NULL,
                details TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                client_name TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'developer',
                created_at REAL NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.commit()


def log_audit_event(event_type: str, name: str, status: str, caller: str = "anonymous", details: str = "") -> None:
    """
    Record an execution or resource access event in the SQLite audit log.
    """
    try:
        init_db()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO audit_logs (timestamp, event_type, name, caller, status, details)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (time.time(), event_type, name, caller, status, details))
            conn.commit()
    except Exception as e:
        # Fallback logging error prevention
        pass


def verify_api_key(key: str) -> dict[str, Any] | None:
    """
    Validate API key and return key record or None if invalid.
    """
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT client_name, role, is_active FROM api_keys WHERE key_hash = ? AND is_active = 1
        """, (key,))
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None


def register_api_key(key: str, client_name: str, role: str = "developer") -> bool:
    """
    Register a new API key in database.
    """
    init_db()
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO api_keys (key_hash, client_name, role, created_at, is_active)
                VALUES (?, ?, ?, ?, 1)
            """, (key, client_name, role, time.time()))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

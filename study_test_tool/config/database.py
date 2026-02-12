"""Database connection handler."""

import sqlite3
from typing import Optional

from config.settings import DB_PATH, SCHEMA_PATH


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a SQLite connection with row factory and foreign keys enabled.

    Args:
        db_path: Optional path override (used for in-memory testing).
                 Defaults to the configured DB_PATH.

    Returns:
        sqlite3.Connection with Row factory and foreign keys ON.
    """
    path = db_path if db_path is not None else str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database(db_path: Optional[str] = None) -> None:
    """Create database tables from schema.sql if they don't exist.

    Args:
        db_path: Optional path override for testing.
    """
    conn = get_connection(db_path)
    try:
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()

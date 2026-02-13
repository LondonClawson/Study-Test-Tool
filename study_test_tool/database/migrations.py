"""Database migration system using PRAGMA user_version."""

import sqlite3
from typing import List, Optional, Tuple

from config.database import get_connection

# Each migration: (version, description, list_of_sql_statements)
MIGRATIONS: List[Tuple[int, str, List[str]]] = [
    (
        1,
        "Add mode column to test_attempts",
        [
            "ALTER TABLE test_attempts ADD COLUMN mode TEXT DEFAULT 'test'",
        ],
    ),
    (
        2,
        "Add indexes for question_responses queries",
        [
            "CREATE INDEX IF NOT EXISTS idx_question_responses_question_id "
            "ON question_responses (question_id)",
            "CREATE INDEX IF NOT EXISTS idx_question_responses_is_correct "
            "ON question_responses (is_correct)",
        ],
    ),
]


def get_schema_version(conn: sqlite3.Connection) -> int:
    """Get the current schema version from PRAGMA user_version."""
    row = conn.execute("PRAGMA user_version").fetchone()
    return row[0] if row else 0


def set_schema_version(conn: sqlite3.Connection, version: int) -> None:
    """Set the schema version via PRAGMA user_version."""
    conn.execute(f"PRAGMA user_version = {version}")


def run_migrations(db_path: Optional[str] = None) -> int:
    """Apply pending migrations to the database.

    Args:
        db_path: Optional path override for testing.

    Returns:
        The final schema version after applying migrations.
    """
    conn = get_connection(db_path)
    try:
        current_version = get_schema_version(conn)

        for version, description, statements in MIGRATIONS:
            if version <= current_version:
                continue

            for sql in statements:
                try:
                    conn.execute(sql)
                except sqlite3.OperationalError as e:
                    # Gracefully handle "column already exists" for fresh installs
                    error_msg = str(e).lower()
                    if "duplicate column" in error_msg or "already exists" in error_msg:
                        continue
                    raise

            set_schema_version(conn, version)
            conn.commit()

        return get_schema_version(conn)
    finally:
        conn.close()

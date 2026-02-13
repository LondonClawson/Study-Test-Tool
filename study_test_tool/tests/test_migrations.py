"""Tests for the database migration system."""

import sqlite3

import pytest

from config.database import initialize_database
from database.migrations import get_schema_version, run_migrations, set_schema_version


class TestMigrations:
    """Tests for schema migration infrastructure."""

    def test_fresh_install_schema_version_zero(self, db_path):
        """Fresh database starts at schema version 0."""
        initialize_database(db_path)
        conn = sqlite3.connect(db_path)
        try:
            version = conn.execute("PRAGMA user_version").fetchone()[0]
            assert version == 0
        finally:
            conn.close()

    def test_run_migrations_applies_all(self, db_path):
        """run_migrations applies all pending migrations."""
        initialize_database(db_path)
        final_version = run_migrations(db_path)
        assert final_version >= 1

    def test_migration_adds_mode_column(self, db_path):
        """Migration 1 adds the mode column to test_attempts."""
        initialize_database(db_path)
        run_migrations(db_path)

        conn = sqlite3.connect(db_path)
        try:
            # Check that mode column exists
            cursor = conn.execute("PRAGMA table_info(test_attempts)")
            columns = {row[1] for row in cursor.fetchall()}
            assert "mode" in columns
        finally:
            conn.close()

    def test_migration_idempotent(self, db_path):
        """Running migrations twice does not error."""
        initialize_database(db_path)
        v1 = run_migrations(db_path)
        v2 = run_migrations(db_path)
        assert v1 == v2

    def test_migration_preserves_data(self, db_path):
        """Migration preserves existing data in test_attempts."""
        initialize_database(db_path)

        # Insert a test and attempt before migration
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            conn.execute(
                "INSERT INTO tests (name, description) VALUES (?, ?)",
                ("Pre-migration Test", "test"),
            )
            conn.execute(
                "INSERT INTO test_attempts (test_id, score, total_questions, "
                "percentage) VALUES (1, 8, 10, 80.0)"
            )
            conn.commit()
        finally:
            conn.close()

        # Run migrations
        run_migrations(db_path)

        # Check data preserved
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            row = conn.execute(
                "SELECT * FROM test_attempts WHERE id = 1"
            ).fetchone()
            assert row is not None
            assert row["score"] == 8
            assert row["percentage"] == 80.0
            # Mode should default to 'test'
            assert row["mode"] == "test"
        finally:
            conn.close()

    def test_migration_adds_response_indexes(self, db_path):
        """Migration 2 adds indexes on question_responses."""
        initialize_database(db_path)
        run_migrations(db_path)

        conn = sqlite3.connect(db_path)
        try:
            indexes = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
            index_names = {row[0] for row in indexes}
            assert "idx_question_responses_question_id" in index_names
            assert "idx_question_responses_is_correct" in index_names
        finally:
            conn.close()

    def test_set_and_get_schema_version(self, db_path):
        """Can set and get schema version."""
        initialize_database(db_path)
        conn = sqlite3.connect(db_path)
        try:
            assert get_schema_version(conn) == 0
            set_schema_version(conn, 5)
            assert get_schema_version(conn) == 5
        finally:
            conn.close()

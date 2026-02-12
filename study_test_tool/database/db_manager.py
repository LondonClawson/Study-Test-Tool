"""Database manager — all SQL operations live here."""

import sqlite3
from typing import Dict, List, Optional

from config.database import get_connection
from models.question import Question, QuestionOption
from models.test import Test
from models.test_result import QuestionResponse, TestAttempt


class DatabaseManager:
    """Centralized CRUD operations for all database tables."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize with optional db_path override for testing."""
        self._db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        """Get a new database connection."""
        return get_connection(self._db_path)

    # ── Test CRUD ──────────────────────────────────────────────

    def create_test(self, test: Test) -> int:
        """Create a new test and return its id."""
        conn = self._conn()
        try:
            cursor = conn.execute(
                "INSERT INTO tests (name, description) VALUES (?, ?)",
                (test.name, test.description),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_all_tests(self) -> List[Test]:
        """Get all tests without loading questions (lazy)."""
        conn = self._conn()
        try:
            rows = conn.execute(
                "SELECT id, name, description, created_at, updated_at "
                "FROM tests ORDER BY updated_at DESC"
            ).fetchall()
            return [
                Test(
                    id=row["id"],
                    name=row["name"],
                    description=row["description"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def get_test_by_id(self, test_id: int) -> Optional[Test]:
        """Get a test with all its questions and options (eager)."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT id, name, description, created_at, updated_at "
                "FROM tests WHERE id = ?",
                (test_id,),
            ).fetchone()
            if not row:
                return None

            test = Test(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            test.questions = self._load_questions(conn, test_id)
            return test
        finally:
            conn.close()

    def update_test(self, test: Test) -> None:
        """Update test name and description."""
        conn = self._conn()
        try:
            conn.execute(
                "UPDATE tests SET name = ?, description = ? WHERE id = ?",
                (test.name, test.description, test.id),
            )
            conn.commit()
        finally:
            conn.close()

    def delete_test(self, test_id: int) -> None:
        """Delete a test and cascade to questions, options, attempts."""
        conn = self._conn()
        try:
            conn.execute("DELETE FROM tests WHERE id = ?", (test_id,))
            conn.commit()
        finally:
            conn.close()

    def get_question_count(self, test_id: int) -> int:
        """Get the number of questions for a test."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM questions WHERE test_id = ?",
                (test_id,),
            ).fetchone()
            return row["cnt"]
        finally:
            conn.close()

    # ── Question CRUD ──────────────────────────────────────────

    def add_question(self, question: Question) -> int:
        """Add a question and return its id."""
        conn = self._conn()
        try:
            cursor = conn.execute(
                "INSERT INTO questions (test_id, question_text, question_type, "
                "correct_answer, category) VALUES (?, ?, ?, ?, ?)",
                (
                    question.test_id,
                    question.text,
                    question.type,
                    question.correct_answer,
                    question.category,
                ),
            )
            question_id = cursor.lastrowid

            for option in question.options:
                conn.execute(
                    "INSERT INTO question_options (question_id, option_text, is_correct) "
                    "VALUES (?, ?, ?)",
                    (question_id, option.text, option.is_correct),
                )

            conn.commit()
            return question_id
        finally:
            conn.close()

    def add_question_option(self, option: QuestionOption) -> int:
        """Add a single option to a question and return its id."""
        conn = self._conn()
        try:
            cursor = conn.execute(
                "INSERT INTO question_options (question_id, option_text, is_correct) "
                "VALUES (?, ?, ?)",
                (option.question_id, option.text, option.is_correct),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_questions_for_test(self, test_id: int) -> List[Question]:
        """Get all questions with options for a test."""
        conn = self._conn()
        try:
            return self._load_questions(conn, test_id)
        finally:
            conn.close()

    def _load_questions(self, conn: sqlite3.Connection, test_id: int) -> List[Question]:
        """Load questions and their options from an open connection."""
        q_rows = conn.execute(
            "SELECT id, test_id, question_text, question_type, correct_answer, "
            "category, created_at FROM questions WHERE test_id = ? ORDER BY id",
            (test_id,),
        ).fetchall()

        questions = []
        for q_row in q_rows:
            question = Question(
                id=q_row["id"],
                test_id=q_row["test_id"],
                text=q_row["question_text"],
                type=q_row["question_type"],
                correct_answer=q_row["correct_answer"],
                category=q_row["category"],
                created_at=q_row["created_at"],
            )

            o_rows = conn.execute(
                "SELECT id, question_id, option_text, is_correct "
                "FROM question_options WHERE question_id = ? ORDER BY id",
                (question.id,),
            ).fetchall()

            question.options = [
                QuestionOption(
                    id=o_row["id"],
                    question_id=o_row["question_id"],
                    text=o_row["option_text"],
                    is_correct=bool(o_row["is_correct"]),
                )
                for o_row in o_rows
            ]
            questions.append(question)

        return questions

    def update_question(self, question: Question) -> None:
        """Update a question's text, type, correct_answer, and category."""
        conn = self._conn()
        try:
            conn.execute(
                "UPDATE questions SET question_text = ?, question_type = ?, "
                "correct_answer = ?, category = ? WHERE id = ?",
                (
                    question.text,
                    question.type,
                    question.correct_answer,
                    question.category,
                    question.id,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def delete_question(self, question_id: int) -> None:
        """Delete a question and cascade to its options."""
        conn = self._conn()
        try:
            conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            conn.commit()
        finally:
            conn.close()

    def delete_options_for_question(self, question_id: int) -> None:
        """Delete all options for a question."""
        conn = self._conn()
        try:
            conn.execute(
                "DELETE FROM question_options WHERE question_id = ?", (question_id,)
            )
            conn.commit()
        finally:
            conn.close()

    # ── Test Attempts ──────────────────────────────────────────

    def save_attempt(self, attempt: TestAttempt) -> int:
        """Save a test attempt and return its id."""
        conn = self._conn()
        try:
            cursor = conn.execute(
                "INSERT INTO test_attempts (test_id, score, total_questions, "
                "percentage, time_taken) VALUES (?, ?, ?, ?, ?)",
                (
                    attempt.test_id,
                    attempt.score,
                    attempt.total_questions,
                    attempt.percentage,
                    attempt.time_taken,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def save_response(self, response: QuestionResponse) -> int:
        """Save a question response and return its id."""
        conn = self._conn()
        try:
            is_correct_val = None
            if response.is_correct is not None:
                is_correct_val = 1 if response.is_correct else 0

            cursor = conn.execute(
                "INSERT INTO question_responses (attempt_id, question_id, "
                "user_answer, is_correct, was_flagged, time_spent) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    response.attempt_id,
                    response.question_id,
                    response.user_answer,
                    is_correct_val,
                    1 if response.was_flagged else 0,
                    response.time_spent,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def get_attempts_for_test(self, test_id: int) -> List[TestAttempt]:
        """Get all attempts for a specific test."""
        conn = self._conn()
        try:
            rows = conn.execute(
                "SELECT a.id, a.test_id, a.score, a.total_questions, "
                "a.percentage, a.time_taken, a.completed_at, t.name as test_name "
                "FROM test_attempts a JOIN tests t ON a.test_id = t.id "
                "WHERE a.test_id = ? ORDER BY a.completed_at DESC",
                (test_id,),
            ).fetchall()
            return [self._row_to_attempt(row) for row in rows]
        finally:
            conn.close()

    def get_all_attempts(self) -> List[TestAttempt]:
        """Get all test attempts across all tests."""
        conn = self._conn()
        try:
            rows = conn.execute(
                "SELECT a.id, a.test_id, a.score, a.total_questions, "
                "a.percentage, a.time_taken, a.completed_at, t.name as test_name "
                "FROM test_attempts a JOIN tests t ON a.test_id = t.id "
                "ORDER BY a.completed_at DESC"
            ).fetchall()
            return [self._row_to_attempt(row) for row in rows]
        finally:
            conn.close()

    def get_attempt_details(self, attempt_id: int) -> Optional[TestAttempt]:
        """Get a test attempt with all its question responses."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT a.id, a.test_id, a.score, a.total_questions, "
                "a.percentage, a.time_taken, a.completed_at, t.name as test_name "
                "FROM test_attempts a JOIN tests t ON a.test_id = t.id "
                "WHERE a.id = ?",
                (attempt_id,),
            ).fetchone()
            if not row:
                return None

            attempt = self._row_to_attempt(row)

            r_rows = conn.execute(
                "SELECT id, attempt_id, question_id, user_answer, is_correct, "
                "was_flagged, time_spent FROM question_responses "
                "WHERE attempt_id = ? ORDER BY id",
                (attempt_id,),
            ).fetchall()

            attempt.responses = [
                QuestionResponse(
                    id=r["id"],
                    attempt_id=r["attempt_id"],
                    question_id=r["question_id"],
                    user_answer=r["user_answer"],
                    is_correct=None if r["is_correct"] is None else bool(r["is_correct"]),
                    was_flagged=bool(r["was_flagged"]),
                    time_spent=r["time_spent"],
                )
                for r in r_rows
            ]
            return attempt
        finally:
            conn.close()

    def get_test_statistics(self, test_id: int) -> Dict:
        """Get statistics for a test: attempt count, average score, best score."""
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT COUNT(*) as attempts, "
                "AVG(percentage) as avg_score, "
                "MAX(percentage) as best_score "
                "FROM test_attempts WHERE test_id = ?",
                (test_id,),
            ).fetchone()
            return {
                "attempts": row["attempts"],
                "avg_score": round(row["avg_score"], 1) if row["avg_score"] else 0.0,
                "best_score": round(row["best_score"], 1) if row["best_score"] else 0.0,
            }
        finally:
            conn.close()

    @staticmethod
    def _row_to_attempt(row: sqlite3.Row) -> TestAttempt:
        """Convert a database row to a TestAttempt."""
        return TestAttempt(
            id=row["id"],
            test_id=row["test_id"],
            score=row["score"],
            total_questions=row["total_questions"],
            percentage=row["percentage"],
            time_taken=row["time_taken"],
            completed_at=row["completed_at"],
            test_name=row["test_name"] if "test_name" in row.keys() else None,
        )

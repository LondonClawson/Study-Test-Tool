"""Tests for practice mode functionality."""

import pytest

from models.test_result import TestAttempt
from services.test_session import TestSession
from models.question import Question, QuestionOption


class TestPracticeModeModel:
    """Tests for the mode field on TestAttempt."""

    def test_attempt_default_mode_is_test(self):
        """TestAttempt defaults to mode='test'."""
        attempt = TestAttempt(test_id=1)
        assert attempt.mode == "test"

    def test_attempt_mode_can_be_practice(self):
        """TestAttempt mode can be set to 'practice'."""
        attempt = TestAttempt(test_id=1, mode="practice")
        assert attempt.mode == "practice"


class TestPracticeModeSession:
    """Tests for the mode parameter on TestSession."""

    def test_session_default_mode(self):
        """TestSession defaults to mode='test'."""
        session = TestSession(test_id=1, questions=[])
        assert session.mode == "test"

    def test_session_practice_mode(self):
        """TestSession accepts mode='practice'."""
        session = TestSession(test_id=1, questions=[], mode="practice")
        assert session.mode == "practice"


class TestPracticeModeDB:
    """Tests for saving/retrieving practice mode attempts."""

    def test_save_attempt_with_mode(self, populated_db):
        """Saving an attempt with mode='practice' persists it."""
        db, test_id = populated_db

        attempt = TestAttempt(
            test_id=test_id,
            score=5,
            total_questions=10,
            percentage=50.0,
            time_taken=100,
            mode="practice",
        )
        attempt_id = db.save_attempt(attempt)

        # Retrieve and check
        details = db.get_attempt_details(attempt_id)
        assert details is not None
        assert details.mode == "practice"

    def test_save_attempt_default_test_mode(self, populated_db):
        """Default mode is 'test' when saved."""
        db, test_id = populated_db

        attempt = TestAttempt(
            test_id=test_id,
            score=8,
            total_questions=10,
            percentage=80.0,
        )
        attempt_id = db.save_attempt(attempt)

        details = db.get_attempt_details(attempt_id)
        assert details.mode == "test"

    def test_get_attempts_by_mode(self, populated_db):
        """get_attempts_by_mode filters correctly."""
        db, test_id = populated_db

        # Create test and practice attempts
        db.save_attempt(TestAttempt(
            test_id=test_id, score=5, total_questions=10,
            percentage=50.0, mode="test",
        ))
        db.save_attempt(TestAttempt(
            test_id=test_id, score=7, total_questions=10,
            percentage=70.0, mode="practice",
        ))
        db.save_attempt(TestAttempt(
            test_id=test_id, score=9, total_questions=10,
            percentage=90.0, mode="test",
        ))

        test_attempts = db.get_attempts_by_mode("test")
        practice_attempts = db.get_attempts_by_mode("practice")

        assert len(test_attempts) == 2
        assert len(practice_attempts) == 1
        assert all(a.mode == "test" for a in test_attempts)
        assert all(a.mode == "practice" for a in practice_attempts)

    def test_get_attempts_by_mode_with_test_id(self, populated_db):
        """get_attempts_by_mode can filter by test_id."""
        db, test_id = populated_db

        db.save_attempt(TestAttempt(
            test_id=test_id, score=5, total_questions=10,
            percentage=50.0, mode="test",
        ))

        results = db.get_attempts_by_mode("test", test_id=test_id)
        assert len(results) == 1
        assert results[0].test_id == test_id

    def test_all_attempts_include_mode(self, populated_db):
        """get_all_attempts returns mode field."""
        db, test_id = populated_db

        db.save_attempt(TestAttempt(
            test_id=test_id, score=5, total_questions=10,
            percentage=50.0, mode="practice",
        ))

        attempts = db.get_all_attempts()
        assert len(attempts) >= 1
        assert any(a.mode == "practice" for a in attempts)

    def test_attempts_for_test_include_mode(self, populated_db):
        """get_attempts_for_test returns mode field."""
        db, test_id = populated_db

        db.save_attempt(TestAttempt(
            test_id=test_id, score=5, total_questions=10,
            percentage=50.0, mode="practice",
        ))

        attempts = db.get_attempts_for_test(test_id)
        assert len(attempts) >= 1
        assert any(a.mode == "practice" for a in attempts)

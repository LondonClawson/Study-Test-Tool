"""Tests for DatabaseManager."""

import pytest

from config.database import get_connection
from models.question import Question, QuestionOption
from models.test import Test
from models.test_result import QuestionResponse, TestAttempt


class TestDatabaseManagerTests:
    """Test CRUD operations."""

    def test_create_and_get_test(self, db):
        test = Test(name="My Test", description="Desc")
        test_id = db.create_test(test)
        assert test_id > 0

        fetched = db.get_test_by_id(test_id)
        assert fetched is not None
        assert fetched.name == "My Test"
        assert fetched.description == "Desc"

    def test_get_all_tests(self, db):
        db.create_test(Test(name="Test 1"))
        db.create_test(Test(name="Test 2"))
        tests = db.get_all_tests()
        assert len(tests) == 2

    def test_update_test(self, db):
        test_id = db.create_test(Test(name="Original"))
        test = db.get_test_by_id(test_id)
        test.name = "Updated"
        db.update_test(test)
        fetched = db.get_test_by_id(test_id)
        assert fetched.name == "Updated"

    def test_delete_test(self, db):
        test_id = db.create_test(Test(name="To Delete"))
        db.delete_test(test_id)
        assert db.get_test_by_id(test_id) is None

    def test_add_question_with_options(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q1?",
            type="multiple_choice",
            correct_answer="A",
            explanation="A is correct because it matches the prompt.",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)
        assert q_id > 0

        questions = db.get_questions_for_test(test_id)
        assert len(questions) == 1
        assert len(questions[0].options) == 2
        assert questions[0].options[0].is_correct is True
        assert questions[0].explanation == "A is correct because it matches the prompt."

    def test_update_question_explanation(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q?",
            type="multiple_choice",
            correct_answer="A",
            explanation="Original explanation.",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)

        q.id = q_id
        q.explanation = "Updated explanation."
        db.update_question(q)

        question = db.get_questions_for_test(test_id)[0]
        assert question.explanation == "Updated explanation."

    def test_delete_question_cascades_options(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q?",
            type="multiple_choice",
            correct_answer="A",
            options=[QuestionOption(text="A", is_correct=True)],
        )
        q_id = db.add_question(q)
        db.delete_question(q_id)
        questions = db.get_questions_for_test(test_id)
        assert len(questions) == 0

    def test_get_question_count(self, populated_db):
        db, test_id = populated_db
        assert db.get_question_count(test_id) == 3

    def test_save_and_get_attempt(self, populated_db):
        db, test_id = populated_db
        attempt = TestAttempt(
            test_id=test_id,
            score=2,
            total_questions=3,
            percentage=66.7,
            time_taken=120,
        )
        attempt_id = db.save_attempt(attempt)
        assert attempt_id > 0

        attempts = db.get_attempts_for_test(test_id)
        assert len(attempts) == 1
        assert attempts[0].score == 2

    def test_save_and_get_responses(self, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)

        attempt = TestAttempt(
            test_id=test_id, score=1, total_questions=3, percentage=50.0
        )
        attempt_id = db.save_attempt(attempt)

        resp = QuestionResponse(
            attempt_id=attempt_id,
            question_id=questions[0].id,
            user_answer="4",
            is_correct=True,
            was_flagged=False,
            time_spent=30,
        )
        db.save_response(resp)

        details = db.get_attempt_details(attempt_id)
        assert details is not None
        assert len(details.responses) == 1
        assert details.responses[0].is_correct is True

    def test_get_test_statistics(self, populated_db):
        db, test_id = populated_db
        db.save_attempt(
            TestAttempt(test_id=test_id, score=2, total_questions=3, percentage=66.7)
        )
        db.save_attempt(
            TestAttempt(test_id=test_id, score=3, total_questions=3, percentage=100.0)
        )
        stats = db.get_test_statistics(test_id)
        assert stats["attempts"] == 2
        assert stats["best_score"] == 100.0

    def test_delete_test_cascades_everything(self, populated_db):
        db, test_id = populated_db
        attempt_id = db.save_attempt(
            TestAttempt(test_id=test_id, score=1, total_questions=3, percentage=33.3)
        )
        questions = db.get_questions_for_test(test_id)
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=questions[0].id,
                user_answer="4",
                is_correct=True,
            )
        )

        db.delete_test(test_id)
        assert db.get_test_by_id(test_id) is None
        assert db.get_questions_for_test(test_id) == []
        assert db.get_attempts_for_test(test_id) == []


class TestGetQuestionHistoryStats:
    """Tests for get_question_history_stats (used by weighted mix selection)."""

    def _insert_attempt(self, db_path, test_id, completed_at):
        conn = get_connection(db_path)
        try:
            cursor = conn.execute(
                "INSERT INTO test_attempts "
                "(test_id, score, total_questions, percentage, time_taken, "
                "mode, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (test_id, 0, 0, 0.0, 0, "test", completed_at),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def test_empty_question_ids_returns_empty_dict(self, db):
        assert db.get_question_history_stats([]) == {}

    def test_unanswered_questions_get_defaults(self, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        qids = [q.id for q in questions]
        stats = db.get_question_history_stats(qids)
        assert set(stats.keys()) == set(qids)
        for qid in qids:
            assert stats[qid] == {
                "last_is_correct": None,
                "last_completed_at": None,
                "attempts_since": 0,
            }

    def test_tracks_last_response_and_attempts_since(self, db_path, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        q = questions[0]

        # Attempt 1 at 10:00 — answered correctly.
        a1 = self._insert_attempt(db_path, test_id, "2026-01-01 10:00:00")
        db.save_response(
            QuestionResponse(
                attempt_id=a1,
                question_id=q.id,
                user_answer="x",
                is_correct=True,
            )
        )

        # Two newer attempts (no response for q) at 10:01 and 10:02.
        self._insert_attempt(db_path, test_id, "2026-01-01 10:01:00")
        self._insert_attempt(db_path, test_id, "2026-01-01 10:02:00")

        stats = db.get_question_history_stats([q.id])
        assert stats[q.id]["last_is_correct"] is True
        assert stats[q.id]["last_completed_at"] == "2026-01-01 10:00:00"
        assert stats[q.id]["attempts_since"] == 2

    def test_essay_response_yields_none_is_correct(self, db_path, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        essay = next(q for q in questions if q.type == "essay")

        a1 = self._insert_attempt(db_path, test_id, "2026-01-01 10:00:00")
        db.save_response(
            QuestionResponse(
                attempt_id=a1,
                question_id=essay.id,
                user_answer="my essay",
                is_correct=None,
            )
        )

        stats = db.get_question_history_stats([essay.id])
        assert stats[essay.id]["last_is_correct"] is None
        assert stats[essay.id]["last_completed_at"] == "2026-01-01 10:00:00"

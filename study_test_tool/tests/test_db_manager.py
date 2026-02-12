"""Tests for DatabaseManager."""

import pytest

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

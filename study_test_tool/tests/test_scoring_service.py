"""Tests for ScoringService."""

import pytest

from models.question import Question, QuestionOption
from services.scoring_service import ScoringService
from services.test_session import TestSession


class TestScoringService:
    """Test scoring logic."""

    def test_score_mc_correct(self):
        q = Question(text="Q?", type="multiple_choice", correct_answer="Yes")
        assert ScoringService.score_question(q, "Yes") is True

    def test_score_mc_incorrect(self):
        q = Question(text="Q?", type="multiple_choice", correct_answer="Yes")
        assert ScoringService.score_question(q, "No") is False

    def test_score_mc_no_answer(self):
        q = Question(text="Q?", type="multiple_choice", correct_answer="Yes")
        assert ScoringService.score_question(q, None) is False

    def test_score_essay_returns_none(self):
        q = Question(text="Explain.", type="essay", correct_answer="Answer")
        assert ScoringService.score_question(q, "My answer") is None

    def test_score_test_all_correct(self):
        questions = [
            Question(
                id=1,
                text="Q1",
                type="multiple_choice",
                correct_answer="A",
                options=[
                    QuestionOption(text="A", is_correct=True),
                    QuestionOption(text="B", is_correct=False),
                ],
            ),
            Question(
                id=2,
                text="Q2",
                type="multiple_choice",
                correct_answer="B",
                options=[
                    QuestionOption(text="A", is_correct=False),
                    QuestionOption(text="B", is_correct=True),
                ],
            ),
        ]

        session = TestSession(test_id=1, questions=questions)
        session.start()
        session.responses = {1: "A", 2: "B"}

        scoring = ScoringService(":memory:")
        result = scoring.score_test(session)

        assert result["score"] == 2
        assert result["total"] == 2
        assert result["percentage"] == 100.0

    def test_score_test_with_essays(self):
        questions = [
            Question(id=1, text="Q1", type="multiple_choice", correct_answer="A"),
            Question(id=2, text="Essay", type="essay", correct_answer="Expected"),
        ]

        session = TestSession(test_id=1, questions=questions)
        session.start()
        session.responses = {1: "A", 2: "My answer"}

        scoring = ScoringService(":memory:")
        result = scoring.score_test(session)

        assert result["score"] == 1
        assert result["total"] == 1  # Only MC counted
        assert result["percentage"] == 100.0
        assert result["essay_questions"] == 1

    def test_score_test_partial(self):
        questions = [
            Question(id=1, text="Q1", type="multiple_choice", correct_answer="A"),
            Question(id=2, text="Q2", type="multiple_choice", correct_answer="B"),
            Question(id=3, text="Q3", type="multiple_choice", correct_answer="C"),
        ]

        session = TestSession(test_id=1, questions=questions)
        session.start()
        session.responses = {1: "A", 2: "Wrong", 3: "C"}

        scoring = ScoringService(":memory:")
        result = scoring.score_test(session)

        assert result["score"] == 2
        assert result["total"] == 3
        assert result["percentage"] == 66.7

    def test_save_attempt(self, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)

        session = TestSession(test_id=test_id, questions=questions)
        session.start()
        session.responses = {questions[0].id: "4", questions[1].id: "Paris"}

        scoring = ScoringService(":memory:")
        # Use the populated_db's db_path for saving
        scoring._db = db
        result = scoring.score_test(session)
        attempt_id = scoring.save_attempt(test_id, result)

        assert attempt_id > 0
        details = db.get_attempt_details(attempt_id)
        assert len(details.responses) == 3  # all questions get a response

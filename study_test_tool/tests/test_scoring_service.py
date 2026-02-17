"""Tests for ScoringService."""

import pytest

from models.question import Question, QuestionOption
from models.test import Test
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

    def test_save_mixed_attempt_creates_per_test_attempts(self, db_path, db):
        """Mixed attempt creates one saved attempt per source test."""
        t1_id = db.create_test(Test(name="Test A"))
        t2_id = db.create_test(Test(name="Test B"))

        q1_id = db.add_question(Question(test_id=t1_id, text="Q1", type="multiple_choice", correct_answer="A"))
        q2_id = db.add_question(Question(test_id=t1_id, text="Q2", type="multiple_choice", correct_answer="B"))
        q3_id = db.add_question(Question(test_id=t2_id, text="Q3", type="multiple_choice", correct_answer="C"))

        q1 = Question(id=q1_id, test_id=t1_id, text="Q1", type="multiple_choice", correct_answer="A")
        q2 = Question(id=q2_id, test_id=t1_id, text="Q2", type="multiple_choice", correct_answer="B")
        q3 = Question(id=q3_id, test_id=t2_id, text="Q3", type="multiple_choice", correct_answer="C")

        session = TestSession(test_id=None, questions=[q1, q2, q3])
        session.start()
        session.responses = {q1_id: "A", q2_id: "Wrong", q3_id: "C"}

        scoring = ScoringService(db_path)
        score_data = scoring.score_test(session)
        attempt_ids = scoring.save_mixed_attempt(score_data, [q1, q2, q3])

        assert len(attempt_ids) == 2  # Two source tests

    def test_save_mixed_attempt_correct_scores(self, db_path, db):
        """Each sub-attempt has the correct score and percentage."""
        t1_id = db.create_test(Test(name="Test A"))
        t2_id = db.create_test(Test(name="Test B"))

        q1_id = db.add_question(Question(test_id=t1_id, text="Q1", type="multiple_choice", correct_answer="A"))
        q2_id = db.add_question(Question(test_id=t1_id, text="Q2", type="multiple_choice", correct_answer="B"))
        q3_id = db.add_question(Question(test_id=t2_id, text="Q3", type="multiple_choice", correct_answer="C"))

        q1 = Question(id=q1_id, test_id=t1_id, text="Q1", type="multiple_choice", correct_answer="A")
        q2 = Question(id=q2_id, test_id=t1_id, text="Q2", type="multiple_choice", correct_answer="B")
        q3 = Question(id=q3_id, test_id=t2_id, text="Q3", type="multiple_choice", correct_answer="C")

        session = TestSession(test_id=None, questions=[q1, q2, q3])
        session.start()
        session.responses = {q1_id: "A", q2_id: "B", q3_id: "Wrong"}

        scoring = ScoringService(db_path)
        score_data = scoring.score_test(session)
        attempt_ids = scoring.save_mixed_attempt(score_data, [q1, q2, q3])

        # Test A attempt: 2/2 = 100%
        a1 = db.get_attempt_details(attempt_ids[0])
        assert a1.score == 2
        assert a1.percentage == 100.0

        # Test B attempt: 0/1 = 0%
        a2 = db.get_attempt_details(attempt_ids[1])
        assert a2.score == 0
        assert a2.percentage == 0.0

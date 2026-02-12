"""Tests for TestSession."""

import time

import pytest

from models.question import Question, QuestionOption
from services.test_session import TestSession


@pytest.fixture
def questions():
    return [
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
            correct_answer="X",
            options=[
                QuestionOption(text="X", is_correct=True),
                QuestionOption(text="Y", is_correct=False),
            ],
        ),
        Question(id=3, text="Essay Q", type="essay", correct_answer="Answer"),
    ]


@pytest.fixture
def session(questions):
    s = TestSession(test_id=1, questions=questions)
    s.start()
    return s


class TestTestSession:
    """Test session state management."""

    def test_initial_state(self, session):
        assert session.current_index == 0
        assert session.total_questions == 3
        assert session.get_unanswered_count() == 3

    def test_get_current_question(self, session):
        q = session.get_current_question()
        assert q.id == 1

    def test_next_question(self, session):
        q = session.next_question()
        assert q.id == 2
        assert session.current_index == 1

    def test_previous_question(self, session):
        session.next_question()
        q = session.previous_question()
        assert q.id == 1
        assert session.current_index == 0

    def test_previous_at_start_returns_none(self, session):
        assert session.previous_question() is None
        assert session.current_index == 0

    def test_next_at_end_returns_none(self, session):
        session.next_question()  # → Q2
        session.next_question()  # → Q3
        assert session.next_question() is None
        assert session.current_index == 2

    def test_go_to_question(self, session):
        q = session.go_to_question(2)
        assert q.id == 3

    def test_go_to_invalid_index(self, session):
        assert session.go_to_question(10) is None
        assert session.current_index == 0

    def test_save_and_retrieve_response(self, session):
        session.save_response(1, "A")
        assert session.responses[1] == "A"
        assert session.get_unanswered_count() == 2

    def test_save_empty_response_removes_it(self, session):
        session.save_response(1, "A")
        session.save_response(1, "")
        assert 1 not in session.responses

    def test_flag_toggle(self, session):
        assert session.flag_question(1) is True  # now flagged
        assert 1 in session.flagged
        assert session.flag_question(1) is False  # unflagged
        assert 1 not in session.flagged

    def test_flagged_count(self, session):
        session.flag_question(1)
        session.flag_question(2)
        assert session.get_flagged_count() == 2

    def test_is_question_answered(self, session):
        assert session.is_question_answered is False
        session.save_response(1, "A")
        assert session.is_question_answered is True

    def test_is_question_flagged(self, session):
        assert session.is_question_flagged is False
        session.flag_question(1)
        assert session.is_question_flagged is True

    def test_elapsed_time(self, session):
        time.sleep(0.1)
        elapsed = session.get_elapsed_time()
        assert elapsed >= 0

    def test_finish_test(self, session):
        session.finish_test()
        # Should not raise
        assert True

"""Shared test fixtures."""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config.database import initialize_database
from database.db_manager import DatabaseManager


@pytest.fixture
def db_path():
    """Return a temporary SQLite file path (cleaned up after test).

    Using :memory: doesn't work because each sqlite3.connect(":memory:")
    creates a separate database — the schema created in one connection
    is invisible to the next.  A temp file lets multiple connections
    share the same database.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def db(db_path):
    """Provide a fresh database with schema applied."""
    initialize_database(db_path)
    return DatabaseManager(db_path)


@pytest.fixture
def populated_db(db):
    """Provide a database with a sample test and questions."""
    from models.question import Question, QuestionOption
    from models.test import Test

    test = Test(name="Sample Test", description="A test for testing")
    test_id = db.create_test(test)

    # MC question
    q1 = Question(
        test_id=test_id,
        text="What is 2 + 2?",
        type="multiple_choice",
        correct_answer="4",
        category="Math",
        options=[
            QuestionOption(text="3", is_correct=False),
            QuestionOption(text="4", is_correct=True),
            QuestionOption(text="5", is_correct=False),
            QuestionOption(text="6", is_correct=False),
        ],
    )
    db.add_question(q1)

    # MC question 2
    q2 = Question(
        test_id=test_id,
        text="What is the capital of France?",
        type="multiple_choice",
        correct_answer="Paris",
        category="Geography",
        options=[
            QuestionOption(text="London", is_correct=False),
            QuestionOption(text="Paris", is_correct=True),
            QuestionOption(text="Berlin", is_correct=False),
        ],
    )
    db.add_question(q2)

    # Essay question
    q3 = Question(
        test_id=test_id,
        text="Explain the theory of relativity.",
        type="essay",
        correct_answer="E = mc^2 and spacetime curvature.",
        category="Physics",
    )
    db.add_question(q3)

    return db, test_id


@pytest.fixture
def db_with_attempts(populated_db):
    """Provide a database with sample attempts and question responses.

    Creates two attempts (one correct, one incorrect) with responses
    for each multiple-choice question.
    """
    from models.test_result import QuestionResponse, TestAttempt

    db, test_id = populated_db

    # Get question IDs
    questions = db.get_questions_for_test(test_id)
    mc_questions = [q for q in questions if q.type == "multiple_choice"]

    # Attempt 1: all correct (test mode)
    attempt1 = TestAttempt(
        test_id=test_id,
        score=2,
        total_questions=3,
        percentage=100.0,
        time_taken=120,
        mode="test",
    )
    attempt1_id = db.save_attempt(attempt1)

    for q in mc_questions:
        db.save_response(
            QuestionResponse(
                attempt_id=attempt1_id,
                question_id=q.id,
                user_answer=q.correct_answer,
                is_correct=True,
            )
        )

    # Attempt 2: first question wrong (practice mode)
    attempt2 = TestAttempt(
        test_id=test_id,
        score=1,
        total_questions=3,
        percentage=50.0,
        time_taken=90,
        mode="practice",
    )
    attempt2_id = db.save_attempt(attempt2)

    for i, q in enumerate(mc_questions):
        is_correct = i > 0  # First MC question wrong
        user_answer = q.correct_answer if is_correct else "wrong answer"
        db.save_response(
            QuestionResponse(
                attempt_id=attempt2_id,
                question_id=q.id,
                user_answer=user_answer,
                is_correct=is_correct,
            )
        )

    # Attempt 3: first question wrong again (test mode) - for frequency data
    attempt3 = TestAttempt(
        test_id=test_id,
        score=1,
        total_questions=3,
        percentage=50.0,
        time_taken=95,
        mode="test",
    )
    attempt3_id = db.save_attempt(attempt3)

    for i, q in enumerate(mc_questions):
        is_correct = i > 0
        user_answer = q.correct_answer if is_correct else "wrong answer"
        db.save_response(
            QuestionResponse(
                attempt_id=attempt3_id,
                question_id=q.id,
                user_answer=user_answer,
                is_correct=is_correct,
            )
        )

    return db, test_id

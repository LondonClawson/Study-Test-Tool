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

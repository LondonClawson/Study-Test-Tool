"""Tests for MixService."""

import pytest

from config.database import initialize_database
from models.question import Question, QuestionOption
from models.test import Test
from services.mix_service import MixService


def _create_two_tests(db):
    """Helper: create two tests with questions and return (test_id_1, test_id_2)."""
    t1 = Test(name="Week 1", description="First week")
    t1_id = db.create_test(t1)

    for i in range(5):
        q = Question(
            test_id=t1_id,
            text=f"W1 Q{i + 1}",
            type="multiple_choice",
            correct_answer="A",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        db.add_question(q)

    t2 = Test(name="Week 2", description="Second week")
    t2_id = db.create_test(t2)

    for i in range(5):
        q = Question(
            test_id=t2_id,
            text=f"W2 Q{i + 1}",
            type="multiple_choice",
            correct_answer="X",
            options=[
                QuestionOption(text="X", is_correct=True),
                QuestionOption(text="Y", is_correct=False),
            ],
        )
        db.add_question(q)

    return t1_id, t2_id


class TestMixService:
    """Tests for MixService.select_questions."""

    def test_select_returns_correct_count(self, db_path, db):
        t1_id, t2_id = _create_two_tests(db)
        service = MixService(db_path)

        result = service.select_questions([t1_id, t2_id], 5)
        assert len(result) == 5

    def test_select_caps_at_available(self, db_path, db):
        t1_id, t2_id = _create_two_tests(db)
        service = MixService(db_path)

        result = service.select_questions([t1_id, t2_id], 100)
        assert len(result) == 10  # 5 + 5

    def test_select_preserves_test_ids(self, db_path, db):
        t1_id, t2_id = _create_two_tests(db)
        service = MixService(db_path)

        result = service.select_questions([t1_id, t2_id], 10, randomize=False)
        valid_ids = {t1_id, t2_id}
        for q in result:
            assert q.test_id in valid_ids

    def test_select_from_single_test(self, db_path, db):
        t1_id, _ = _create_two_tests(db)
        service = MixService(db_path)

        result = service.select_questions([t1_id], 3)
        assert len(result) == 3
        for q in result:
            assert q.test_id == t1_id

    def test_select_empty_test_ids(self, db_path, db):
        service = MixService(db_path)
        result = service.select_questions([], 10)
        assert result == []

    def test_select_zero_count(self, db_path, db):
        t1_id, _ = _create_two_tests(db)
        service = MixService(db_path)

        result = service.select_questions([t1_id], 0)
        assert result == []

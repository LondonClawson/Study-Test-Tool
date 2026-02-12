"""Tests for RandomizerService."""

import pytest

from models.question import Question, QuestionOption
from services.randomizer_service import RandomizerService


@pytest.fixture
def questions():
    return [
        Question(
            id=i,
            text=f"Question {i}",
            type="multiple_choice",
            correct_answer=f"Opt {i}A",
            options=[
                QuestionOption(text=f"Opt {i}A", is_correct=True),
                QuestionOption(text=f"Opt {i}B", is_correct=False),
                QuestionOption(text=f"Opt {i}C", is_correct=False),
                QuestionOption(text=f"Opt {i}D", is_correct=False),
            ],
        )
        for i in range(1, 11)
    ]


class TestRandomizerService:
    """Test shuffling operations."""

    def test_shuffle_questions_returns_same_items(self, questions):
        shuffled = RandomizerService.shuffle_questions(questions)
        assert len(shuffled) == len(questions)
        assert set(q.id for q in shuffled) == set(q.id for q in questions)

    def test_shuffle_questions_does_not_mutate_original(self, questions):
        original_ids = [q.id for q in questions]
        RandomizerService.shuffle_questions(questions)
        assert [q.id for q in questions] == original_ids

    def test_shuffle_options_preserves_correct_answer(self, questions):
        q = questions[0]
        shuffled = RandomizerService.shuffle_options(q)
        correct_opts = [o for o in shuffled.options if o.is_correct]
        assert len(correct_opts) == 1
        assert correct_opts[0].text == "Opt 1A"

    def test_shuffle_options_does_not_mutate_original(self, questions):
        q = questions[0]
        original_order = [o.text for o in q.options]
        RandomizerService.shuffle_options(q)
        assert [o.text for o in q.options] == original_order

    def test_shuffle_all_shuffles_both(self, questions):
        shuffled = RandomizerService.shuffle_all(questions)
        assert len(shuffled) == len(questions)
        # Each question should still have correct answer
        for q in shuffled:
            correct_opts = [o for o in q.options if o.is_correct]
            assert len(correct_opts) == 1

    def test_shuffle_actually_changes_order(self, questions):
        """With 10 questions, shuffling should change order at least sometimes."""
        orders = set()
        for _ in range(20):
            shuffled = RandomizerService.shuffle_questions(questions)
            order = tuple(q.id for q in shuffled)
            orders.add(order)
        # Should have more than 1 unique ordering in 20 tries
        assert len(orders) > 1

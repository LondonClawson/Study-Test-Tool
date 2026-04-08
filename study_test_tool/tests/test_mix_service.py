"""Tests for MixService."""

import random

import pytest

from config.database import initialize_database, get_connection
from models.question import Question, QuestionOption
from models.test import Test
from models.test_result import QuestionResponse, TestAttempt
from services.mix_service import (
    MixService,
    RECOVERY_ATTEMPTS,
    WEIGHT_FLOOR,
    _compute_weight,
    _weighted_sample_without_replacement,
)


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


def _insert_attempt_with_timestamp(
    db_path: str, test_id: int, completed_at: str
) -> int:
    """Insert a test_attempts row with an explicit completed_at (ISO string).

    Needed because ``save_attempt`` relies on SQLite's CURRENT_TIMESTAMP
    default, which has second-level resolution and produces ties for
    attempts created in quick succession during tests.
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.execute(
            "INSERT INTO test_attempts "
            "(test_id, score, total_questions, percentage, time_taken, mode, "
            "completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (test_id, 0, 0, 0.0, 0, "test", completed_at),
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def _insert_response(
    db_path: str,
    attempt_id: int,
    question_id: int,
    is_correct,
) -> None:
    """Insert a question_responses row with a specific is_correct value."""
    conn = get_connection(db_path)
    try:
        if is_correct is None:
            value = None
        else:
            value = 1 if is_correct else 0
        conn.execute(
            "INSERT INTO question_responses "
            "(attempt_id, question_id, user_answer, is_correct, was_flagged, "
            "time_spent) VALUES (?, ?, ?, ?, ?, ?)",
            (attempt_id, question_id, "", value, 0, 0),
        )
        conn.commit()
    finally:
        conn.close()


def _ts(minute: int) -> str:
    """Build an ISO timestamp varying only by minute, for deterministic ordering."""
    return f"2026-01-01 10:{minute:02d}:00"


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


class TestComputeWeight:
    """Unit tests for the _compute_weight helper."""

    def test_unseen_question_gets_max_weight(self):
        stats = {
            "last_is_correct": None,
            "last_completed_at": None,
            "attempts_since": 0,
        }
        assert _compute_weight(stats) == 1.0

    def test_last_incorrect_gets_max_weight(self):
        stats = {
            "last_is_correct": False,
            "last_completed_at": "x",
            "attempts_since": 0,
        }
        assert _compute_weight(stats) == 1.0

    def test_correct_last_attempt_hits_floor(self):
        stats = {
            "last_is_correct": True,
            "last_completed_at": "x",
            "attempts_since": 0,
        }
        assert _compute_weight(stats) == pytest.approx(WEIGHT_FLOOR)

    def test_correct_recovers_linearly(self):
        expected_at_3 = WEIGHT_FLOOR + (1.0 - WEIGHT_FLOOR) * (3 / RECOVERY_ATTEMPTS)
        stats = {
            "last_is_correct": True,
            "last_completed_at": "x",
            "attempts_since": 3,
        }
        assert _compute_weight(stats) == pytest.approx(expected_at_3)

    def test_correct_fully_recovers_at_or_past_recovery(self):
        for k in (RECOVERY_ATTEMPTS, RECOVERY_ATTEMPTS + 10):
            stats = {
                "last_is_correct": True,
                "last_completed_at": "x",
                "attempts_since": k,
            }
            assert _compute_weight(stats) == pytest.approx(1.0)


class TestWeightedSampleWithoutReplacement:
    """Unit tests for the Efraimidis–Spirakis helper."""

    def test_returns_requested_count(self):
        items = list(range(10))
        weights = [1.0] * 10
        result = _weighted_sample_without_replacement(items, weights, 5)
        assert len(result) == 5
        assert len(set(result)) == 5  # no duplicates

    def test_zero_k_returns_empty(self):
        assert _weighted_sample_without_replacement([1, 2, 3], [1, 1, 1], 0) == []

    def test_empty_items_returns_empty(self):
        assert _weighted_sample_without_replacement([], [], 3) == []

    def test_higher_weight_selected_more_often(self):
        random.seed(1234)
        counts = {"a": 0, "b": 0}
        trials = 2000
        for _ in range(trials):
            result = _weighted_sample_without_replacement(
                ["a", "b"], [0.1, 1.0], 1
            )
            counts[result[0]] += 1
        # With weights 0.1 vs 1.0, "b" should dominate heavily.
        assert counts["b"] > counts["a"] * 3


class TestMixServiceWeighting:
    """Integration tests for history-aware question selection."""

    def test_fresh_db_behaves_like_uniform(self, db_path, db):
        """With no history, every question has weight 1.0 and distribution is uniform."""
        t1_id, t2_id = _create_two_tests(db)
        service = MixService(db_path)
        random.seed(42)
        counts = {}
        trials = 500
        for _ in range(trials):
            result = service.select_questions([t1_id, t2_id], 1, randomize=False)
            counts[result[0].id] = counts.get(result[0].id, 0) + 1
        # 10 questions, ~50 picks each. Allow generous tolerance.
        for qid, c in counts.items():
            assert 20 < c < 100, f"question {qid} picked {c} times"

    def test_recently_correct_questions_picked_less(self, db_path, db):
        """A question answered correctly in the most recent attempt should be
        selected noticeably less often than unseen questions."""
        t1_id, _ = _create_two_tests(db)
        questions = db.get_questions_for_test(t1_id)
        target = questions[0]

        attempt_id = _insert_attempt_with_timestamp(db_path, t1_id, _ts(0))
        _insert_response(db_path, attempt_id, target.id, is_correct=True)

        service = MixService(db_path)
        random.seed(7)
        counts = {}
        trials = 1000
        for _ in range(trials):
            result = service.select_questions([t1_id], 1, randomize=False)
            counts[result[0].id] = counts.get(result[0].id, 0) + 1

        target_count = counts.get(target.id, 0)
        # The 4 unseen questions should each be picked ~6x more often than the
        # penalized one (since weight is 0.1 vs 1.0 and k=0).
        other_counts = [c for qid, c in counts.items() if qid != target.id]
        avg_other = sum(other_counts) / len(other_counts)
        assert target_count < avg_other / 2, (
            f"target picked {target_count}, avg other {avg_other}"
        )

    def test_recently_incorrect_gets_full_weight(self, db_path, db):
        """A question answered incorrectly most recently should be picked at
        roughly the same rate as unseen questions."""
        t1_id, _ = _create_two_tests(db)
        questions = db.get_questions_for_test(t1_id)
        wrong_q = questions[0]

        attempt_id = _insert_attempt_with_timestamp(db_path, t1_id, _ts(0))
        _insert_response(db_path, attempt_id, wrong_q.id, is_correct=False)

        service = MixService(db_path)
        random.seed(11)
        counts = {}
        trials = 1000
        for _ in range(trials):
            result = service.select_questions([t1_id], 1, randomize=False)
            counts[result[0].id] = counts.get(result[0].id, 0) + 1

        wrong_count = counts.get(wrong_q.id, 0)
        other_counts = [c for qid, c in counts.items() if qid != wrong_q.id]
        avg_other = sum(other_counts) / len(other_counts)
        # Should be within ~30% of the average of unseen questions.
        assert abs(wrong_count - avg_other) / avg_other < 0.3

    def test_correct_weight_recovers_after_recovery_attempts(self, db_path, db):
        """After RECOVERY_ATTEMPTS subsequent attempts, a previously-correct
        question should be back at full weight."""
        t1_id, _ = _create_two_tests(db)
        questions = db.get_questions_for_test(t1_id)
        target = questions[0]

        # Attempt at minute 0: target correct.
        a0 = _insert_attempt_with_timestamp(db_path, t1_id, _ts(0))
        _insert_response(db_path, a0, target.id, is_correct=True)

        # 5 more unrelated attempts at later timestamps.
        for i in range(1, RECOVERY_ATTEMPTS + 1):
            _insert_attempt_with_timestamp(db_path, t1_id, _ts(i))

        service = MixService(db_path)
        random.seed(19)
        counts = {}
        trials = 1000
        for _ in range(trials):
            result = service.select_questions([t1_id], 1, randomize=False)
            counts[result[0].id] = counts.get(result[0].id, 0) + 1

        target_count = counts.get(target.id, 0)
        other_counts = [c for qid, c in counts.items() if qid != target.id]
        avg_other = sum(other_counts) / len(other_counts)
        # Should be within ~30% of average — weight has fully recovered.
        assert abs(target_count - avg_other) / avg_other < 0.3

    def test_essay_response_treated_as_unseen(self, db_path, db):
        """An essay response (is_correct=NULL) should not penalize the question."""
        t1_id, _ = _create_two_tests(db)
        questions = db.get_questions_for_test(t1_id)
        essay_target = questions[0]

        attempt_id = _insert_attempt_with_timestamp(db_path, t1_id, _ts(0))
        _insert_response(db_path, attempt_id, essay_target.id, is_correct=None)

        service = MixService(db_path)
        random.seed(23)
        counts = {}
        trials = 1000
        for _ in range(trials):
            result = service.select_questions([t1_id], 1, randomize=False)
            counts[result[0].id] = counts.get(result[0].id, 0) + 1

        target_count = counts.get(essay_target.id, 0)
        other_counts = [c for qid, c in counts.items() if qid != essay_target.id]
        avg_other = sum(other_counts) / len(other_counts)
        assert abs(target_count - avg_other) / avg_other < 0.3

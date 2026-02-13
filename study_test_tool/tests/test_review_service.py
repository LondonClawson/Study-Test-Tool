"""Tests for the review service and missed questions functionality."""

import pytest

from services.review_service import ReviewService


class TestMissedQuestions:
    """Tests for missed questions retrieval."""

    def test_get_missed_questions(self, db_with_attempts):
        """Missed questions are returned with stats."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        assert len(missed) >= 1

        # The first MC question was missed in attempts 2 and 3
        q = missed[0]
        assert "question_id" in q
        assert "question_text" in q
        assert "times_missed" in q
        assert "total_attempts" in q
        assert q["times_missed"] > 0

    def test_get_missed_questions_by_test(self, db_with_attempts):
        """Can filter missed questions by test_id."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions(test_id=test_id)
        assert all(m["test_id"] == test_id for m in missed)

    def test_get_missed_questions_returns_test_name(self, db_with_attempts):
        """Missed questions include test_name."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        assert all(m.get("test_name") for m in missed)

    def test_get_missed_questions_returns_category(self, db_with_attempts):
        """Missed questions include category."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        for m in missed:
            assert "category" in m


class TestFrequentlyMissed:
    """Tests for frequently missed questions filtering."""

    def test_frequently_missed_threshold(self, db_with_attempts):
        """Frequently missed filters by min_attempts and miss_threshold."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        # With low thresholds, should return results
        freq = service.get_frequently_missed(
            min_attempts=2, miss_threshold=0.5
        )
        # The first MC question was missed 2/3 times (66%), above 50%
        assert len(freq) >= 1

    def test_frequently_missed_high_threshold(self, db_with_attempts):
        """High threshold filters out less-frequently missed questions."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        freq = service.get_frequently_missed(
            min_attempts=2, miss_threshold=0.9
        )
        # 66% miss rate is below 90% threshold
        assert len(freq) == 0

    def test_frequently_missed_by_test(self, db_with_attempts):
        """Can filter frequently missed by test_id."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        freq = service.get_frequently_missed(
            test_id=test_id, min_attempts=2, miss_threshold=0.5
        )
        assert all(f["test_id"] == test_id for f in freq)


class TestGetQuestionById:
    """Tests for get_question_by_id in the database manager."""

    def test_get_question_by_id(self, populated_db):
        """Can retrieve a single question by ID."""
        db, test_id = populated_db

        questions = db.get_questions_for_test(test_id)
        first_q = questions[0]

        retrieved = db.get_question_by_id(first_q.id)
        assert retrieved is not None
        assert retrieved.id == first_q.id
        assert retrieved.text == first_q.text

    def test_get_question_by_id_includes_options(self, populated_db):
        """get_question_by_id loads options."""
        db, test_id = populated_db

        questions = db.get_questions_for_test(test_id)
        mc_q = [q for q in questions if q.type == "multiple_choice"][0]

        retrieved = db.get_question_by_id(mc_q.id)
        assert len(retrieved.options) > 0

    def test_get_question_by_id_not_found(self, db):
        """Returns None for nonexistent question ID."""
        result = db.get_question_by_id(9999)
        assert result is None


class TestCreateReviewSession:
    """Tests for creating review sessions from question IDs."""

    def test_create_review_session_questions(self, db_with_attempts):
        """Can load full Question objects from IDs."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        ids = [m["question_id"] for m in missed]

        questions = service.create_review_session_questions(ids)
        assert len(questions) == len(ids)
        for q in questions:
            assert q.id in ids

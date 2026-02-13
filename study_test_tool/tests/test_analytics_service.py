"""Tests for the analytics service and weak topic identification."""

import pytest

from services.analytics_service import AnalyticsService


class TestScoresOverTime:
    """Tests for score trends data retrieval."""

    def test_scores_over_time(self, db_with_attempts):
        """Returns chronological score data."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        scores = service.get_scores_over_time()
        assert len(scores) >= 1
        for s in scores:
            assert "percentage" in s
            assert "completed_at" in s
            assert "test_name" in s

    def test_scores_over_time_by_test(self, db_with_attempts):
        """Can filter scores by test_id."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        scores = service.get_scores_over_time(test_id=test_id)
        assert len(scores) >= 1

    def test_scores_over_time_by_mode(self, db_with_attempts):
        """Can filter scores by mode."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        test_scores = service.get_scores_over_time(mode="test")
        practice_scores = service.get_scores_over_time(mode="practice")

        # We created 2 test-mode and 1 practice-mode attempt
        assert len(test_scores) >= 1
        assert len(practice_scores) >= 1

    def test_scores_over_time_empty(self, db):
        """Returns empty list when no data."""
        service = AnalyticsService(db._db_path)
        scores = service.get_scores_over_time()
        assert scores == []


class TestAverageScoresByTest:
    """Tests for test comparison data."""

    def test_average_scores_by_test(self, db_with_attempts):
        """Returns per-test aggregate stats."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        avgs = service.get_average_scores_by_test()
        assert len(avgs) >= 1

        for a in avgs:
            assert "test_name" in a
            assert "avg_score" in a
            assert "best_score" in a
            assert "attempt_count" in a
            assert a["attempt_count"] >= 1

    def test_average_scores_by_mode(self, db_with_attempts):
        """Filters by mode."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        test_avgs = service.get_average_scores_by_test(mode="test")
        assert len(test_avgs) >= 1


class TestAttemptFrequency:
    """Tests for study activity data."""

    def test_attempt_frequency(self, db_with_attempts):
        """Returns daily attempt counts."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        freq = service.get_attempt_frequency(days=30)
        assert len(freq) >= 1
        for f in freq:
            assert "day" in f
            assert "count" in f
            assert f["count"] >= 1

    def test_attempt_frequency_empty(self, db):
        """Returns empty list when no data."""
        service = AnalyticsService(db._db_path)
        freq = service.get_attempt_frequency()
        assert freq == []


class TestCategoryPerformance:
    """Tests for category-level analytics."""

    def test_category_performance(self, db_with_attempts):
        """Returns correct/total/percentage per category."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        cats = service.get_category_performance()
        assert len(cats) >= 1

        for c in cats:
            assert "category" in c
            assert "total" in c
            assert "correct" in c
            assert "percentage" in c
            assert c["category"] != ""

    def test_category_performance_by_test(self, db_with_attempts):
        """Can filter by test_id."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        cats = service.get_category_performance(test_id=test_id)
        assert len(cats) >= 1


class TestWeakTopics:
    """Tests for weak topic identification."""

    def test_weak_topics_classification(self, db_with_attempts):
        """Topics are classified as weak/moderate/strong."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        topics = service.get_weak_topics()
        assert len(topics) >= 1

        for t in topics:
            assert "status" in t
            assert t["status"] in ("weak", "moderate", "strong")

    def test_weak_topics_threshold(self, db_with_attempts):
        """Weak status is below threshold, strong is above 85%."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        topics = service.get_weak_topics(threshold=70.0)
        for t in topics:
            if t["percentage"] < 70.0:
                assert t["status"] == "weak"
            elif t["percentage"] < 85.0:
                assert t["status"] == "moderate"
            else:
                assert t["status"] == "strong"

    def test_weak_topics_custom_threshold(self, db_with_attempts):
        """Custom threshold changes classification."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        # With very high threshold, more topics should be "weak"
        topics_high = service.get_weak_topics(threshold=99.0)
        weak_count = sum(1 for t in topics_high if t["status"] == "weak")

        # With very low threshold, fewer should be "weak"
        topics_low = service.get_weak_topics(threshold=1.0)
        weak_count_low = sum(1 for t in topics_low if t["status"] == "weak")

        assert weak_count >= weak_count_low

    def test_weak_topics_by_test(self, db_with_attempts):
        """Can filter weak topics by test_id."""
        db, test_id = db_with_attempts
        service = AnalyticsService(db._db_path)

        topics = service.get_weak_topics(test_id=test_id)
        assert len(topics) >= 1

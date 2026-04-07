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

    def test_fallback_to_test_name_when_no_categories(self, db):
        """Without categories or group_name, falls back to grouping by test name."""
        from models.question import Question, QuestionOption
        from models.test import Test
        from models.test_result import QuestionResponse, TestAttempt

        test = Test(name="Untagged Test")
        test_id = db.create_test(test)

        q = Question(
            test_id=test_id,
            text="Q1",
            type="multiple_choice",
            correct_answer="A",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)

        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id, score=0, total_questions=1, percentage=0.0
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=q_id,
                user_answer="B",
                is_correct=False,
            )
        )

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance()
        assert len(cats) == 1
        assert cats[0]["category"] == "Untagged Test"
        assert cats[0]["total"] == 1
        assert cats[0]["correct"] == 0

    def test_fallback_collapses_tests_sharing_group_name(self, db):
        """Tests with the same group_name collapse into a single bucket."""
        from models.question import Question, QuestionOption
        from models.test import Test
        from models.test_result import QuestionResponse, TestAttempt

        test_a_id = db.create_test(Test(name="Test A", group_name="Shared"))
        test_b_id = db.create_test(Test(name="Test B", group_name="Shared"))

        for tid, correct in [(test_a_id, True), (test_b_id, False)]:
            q = Question(
                test_id=tid,
                text="Q",
                type="multiple_choice",
                correct_answer="A",
                options=[
                    QuestionOption(text="A", is_correct=True),
                    QuestionOption(text="B", is_correct=False),
                ],
            )
            q_id = db.add_question(q)
            attempt_id = db.save_attempt(
                TestAttempt(
                    test_id=tid, score=0, total_questions=1, percentage=0.0
                )
            )
            db.save_response(
                QuestionResponse(
                    attempt_id=attempt_id,
                    question_id=q_id,
                    user_answer="A" if correct else "B",
                    is_correct=correct,
                )
            )

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance()
        assert len(cats) == 1
        assert cats[0]["category"] == "Shared"
        assert cats[0]["total"] == 2
        assert cats[0]["correct"] == 1
        assert cats[0]["percentage"] == 50.0

    def test_categorized_questions_take_priority_over_fallback(self, db):
        """If any in-scope question has a category, only categorized rows are returned."""
        from models.question import Question, QuestionOption
        from models.test import Test
        from models.test_result import QuestionResponse, TestAttempt

        test_id = db.create_test(Test(name="Mixed Test", group_name="Grouped"))

        tagged = Question(
            test_id=test_id,
            text="Tagged",
            type="multiple_choice",
            correct_answer="A",
            category="Algebra",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        tagged_id = db.add_question(tagged)

        untagged = Question(
            test_id=test_id,
            text="Untagged",
            type="multiple_choice",
            correct_answer="A",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        untagged_id = db.add_question(untagged)

        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id, score=2, total_questions=2, percentage=100.0
            )
        )
        for qid in (tagged_id, untagged_id):
            db.save_response(
                QuestionResponse(
                    attempt_id=attempt_id,
                    question_id=qid,
                    user_answer="A",
                    is_correct=True,
                )
            )

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance()
        assert [c["category"] for c in cats] == ["Algebra"]
        assert cats[0]["total"] == 1


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


def _seed_two_tests_one_group(db):
    """Two tests sharing a group, no per-question category; one response each."""
    from models.question import Question, QuestionOption
    from models.test import Test
    from models.test_result import QuestionResponse, TestAttempt

    test_a_id = db.create_test(Test(name="Test A", group_name="Shared"))
    test_b_id = db.create_test(Test(name="Test B", group_name="Shared"))

    ids = {}
    for tid, correct in [(test_a_id, True), (test_b_id, False)]:
        q = Question(
            test_id=tid,
            text="Q",
            type="multiple_choice",
            correct_answer="A",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)
        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=tid, score=0, total_questions=1, percentage=0.0
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=q_id,
                user_answer="A" if correct else "B",
                is_correct=correct,
            )
        )
        ids[tid] = q_id
    return test_a_id, test_b_id


class TestGroupByModes:
    """Tests for the explicit group_by parameter on category performance."""

    def test_group_by_test_splits_into_per_test_rows(self, db):
        """group_by='test' returns one row per test even when they share a group."""
        _seed_two_tests_one_group(db)

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance(group_by="test")

        labels = sorted(c["category"] for c in cats)
        assert labels == ["Test A", "Test B"]
        for c in cats:
            assert c["total"] == 1

    def test_group_by_group_collapses_shared_group(self, db):
        """group_by='group' buckets tests sharing a group_name together."""
        _seed_two_tests_one_group(db)

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance(group_by="group")

        assert len(cats) == 1
        assert cats[0]["category"] == "Shared"
        assert cats[0]["total"] == 2
        assert cats[0]["correct"] == 1

    def test_group_by_group_falls_back_to_test_name_when_empty(self, db):
        """group_by='group' uses test name when group_name is unset."""
        from models.question import Question, QuestionOption
        from models.test import Test
        from models.test_result import QuestionResponse, TestAttempt

        test_id = db.create_test(Test(name="Solo Test"))
        q = Question(
            test_id=test_id,
            text="Q",
            type="multiple_choice",
            correct_answer="A",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)
        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id, score=1, total_questions=1, percentage=100.0
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=q_id,
                user_answer="A",
                is_correct=True,
            )
        )

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance(group_by="group")
        assert len(cats) == 1
        assert cats[0]["category"] == "Solo Test"

    def test_group_by_category_returns_empty_when_no_categories(self, db):
        """Explicit group_by='category' does NOT fall back — returns []."""
        _seed_two_tests_one_group(db)

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance(group_by="category")
        assert cats == []

    def test_group_by_category_returns_category_rows_when_tagged(self, db):
        """group_by='category' lists per-category stats when tags exist."""
        from models.question import Question, QuestionOption
        from models.test import Test
        from models.test_result import QuestionResponse, TestAttempt

        test_id = db.create_test(Test(name="Mixed"))
        q = Question(
            test_id=test_id,
            text="Tagged",
            type="multiple_choice",
            correct_answer="A",
            category="Algebra",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)
        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id, score=1, total_questions=1, percentage=100.0
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=q_id,
                user_answer="A",
                is_correct=True,
            )
        )

        service = AnalyticsService(db._db_path)
        cats = service.get_category_performance(group_by="category")
        assert [c["category"] for c in cats] == ["Algebra"]

    def test_group_by_auto_preserves_legacy_fallback(self, db):
        """group_by='auto' (the default) still falls back to group/test name."""
        _seed_two_tests_one_group(db)

        service = AnalyticsService(db._db_path)
        cats_auto = service.get_category_performance(group_by="auto")
        cats_default = service.get_category_performance()
        assert cats_auto == cats_default
        assert len(cats_auto) == 1
        assert cats_auto[0]["category"] == "Shared"

    def test_weak_topics_passes_group_by_through(self, db):
        """get_weak_topics forwards group_by and still classifies status."""
        _seed_two_tests_one_group(db)

        service = AnalyticsService(db._db_path)
        topics = service.get_weak_topics(group_by="test")
        labels = sorted(t["category"] for t in topics)
        assert labels == ["Test A", "Test B"]
        for t in topics:
            assert t["status"] in ("weak", "moderate", "strong")

    def test_invalid_group_by_raises(self, db):
        """Unsupported group_by value raises ValueError."""
        service = AnalyticsService(db._db_path)
        with pytest.raises(ValueError):
            service.get_category_performance(group_by="tag")
        with pytest.raises(ValueError):
            service.get_weak_topics(group_by="bogus")

"""Tests for the review service and missed questions functionality."""

import pytest

from models.question import Question, QuestionOption
from models.test import Test
from models.test_result import QuestionResponse, TestAttempt
from services.review_service import ReviewService


def _create_missed_test(db, name, group_name=""):
    """Create a one-question test with enough misses for frequency tests."""
    test_id = db.create_test(Test(name=name, group_name=group_name))
    question_id = db.add_question(
        Question(
            test_id=test_id,
            text=f"{name} missed question",
            type="multiple_choice",
            correct_answer="A",
            category=group_name,
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
    )

    for _ in range(2):
        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id,
                score=0,
                total_questions=1,
                percentage=0.0,
                mode="test",
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=question_id,
                user_answer="B",
                is_correct=False,
            )
        )

    return test_id, question_id


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

    def test_get_missed_questions_excludes_archived_tests(self, db):
        """All missed review excludes archived tests."""
        archived_test_id, archived_question_id = _create_missed_test(
            db, "Last Semester Exam", "Class 1"
        )
        active_test_id, active_question_id = _create_missed_test(
            db, "Current Semester Quiz", "Class 2"
        )
        db.archive_test(archived_test_id)
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        question_ids = {item["question_id"] for item in missed}

        assert active_question_id in question_ids
        assert archived_question_id not in question_ids
        assert all(item["test_id"] != archived_test_id for item in missed)
        assert all(item["test_id"] == active_test_id for item in missed)

    def test_get_missed_questions_excludes_archived_test_id(self, db):
        """Explicit archived test filters still return no review questions."""
        archived_test_id, _ = _create_missed_test(db, "Archived Quiz", "Class 1")
        db.archive_test(archived_test_id)
        service = ReviewService(db._db_path)

        assert service.get_missed_questions(test_id=archived_test_id) == []

    def test_get_missed_questions_filters_multiple_tests(self, db):
        """Can review missed questions from selected active tests."""
        first_test_id, first_question_id = _create_missed_test(db, "Quiz 1", "Class 2")
        second_test_id, second_question_id = _create_missed_test(
            db, "Quiz 2", "Class 2"
        )
        third_test_id, third_question_id = _create_missed_test(db, "Quiz 3", "Class 2")
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions(test_ids=[first_test_id, second_test_id])
        question_ids = {item["question_id"] for item in missed}

        assert question_ids == {first_question_id, second_question_id}
        assert third_question_id not in question_ids
        assert all(item["test_id"] != third_test_id for item in missed)

    def test_get_missed_questions_rejects_conflicting_filters(self, db_with_attempts):
        """Callers must choose either single-test or multi-test filtering."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        with pytest.raises(ValueError):
            service.get_missed_questions(test_id=test_id, test_ids=[test_id])


class TestFrequentlyMissed:
    """Tests for frequently missed questions filtering."""

    def test_frequently_missed_threshold(self, db_with_attempts):
        """Frequently missed filters by min_attempts and miss_threshold."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        # With low thresholds, should return results
        freq = service.get_frequently_missed(min_attempts=2, miss_threshold=0.5)
        # The first MC question was missed 2/3 times (66%), above 50%
        assert len(freq) >= 1

    def test_frequently_missed_high_threshold(self, db_with_attempts):
        """High threshold filters out less-frequently missed questions."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        freq = service.get_frequently_missed(min_attempts=2, miss_threshold=0.9)
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

    def test_frequently_missed_excludes_archived_tests(self, db):
        """Frequently missed review excludes archived tests."""
        archived_test_id, archived_question_id = _create_missed_test(
            db, "Old Final", "Class 1"
        )
        active_test_id, active_question_id = _create_missed_test(
            db, "New Quiz", "Class 2"
        )
        db.archive_test(archived_test_id)
        service = ReviewService(db._db_path)

        freq = service.get_frequently_missed(min_attempts=2, miss_threshold=0.5)
        question_ids = {item["question_id"] for item in freq}

        assert active_question_id in question_ids
        assert archived_question_id not in question_ids
        assert all(item["test_id"] == active_test_id for item in freq)

    def test_frequently_missed_filters_multiple_tests(self, db):
        """Frequently missed can be scoped to selected active tests."""
        first_test_id, first_question_id = _create_missed_test(db, "Quiz 1", "Class 2")
        second_test_id, second_question_id = _create_missed_test(
            db, "Quiz 2", "Class 2"
        )
        third_test_id, third_question_id = _create_missed_test(db, "Quiz 3", "Class 2")
        service = ReviewService(db._db_path)

        freq = service.get_frequently_missed(
            min_attempts=2,
            miss_threshold=0.5,
            test_ids=[first_test_id, second_test_id],
        )
        question_ids = {item["question_id"] for item in freq}

        assert question_ids == {first_question_id, second_question_id}
        assert third_question_id not in question_ids
        assert all(item["test_id"] != third_test_id for item in freq)

    def test_frequently_missed_rejects_conflicting_filters(self, db_with_attempts):
        """Callers must choose either single-test or multi-test filtering."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        with pytest.raises(ValueError):
            service.get_frequently_missed(
                test_id=test_id,
                test_ids=[test_id],
                min_attempts=2,
                miss_threshold=0.5,
            )


class TestMissedQuestionPagination:
    """Tests for bounded Review retrieval and totals."""

    def test_missed_question_pages_have_stable_order_and_total(self, db):
        """Paged missed questions retain a stable order across offsets."""
        question_ids = []
        for index in range(5):
            _, question_id = _create_missed_test(db, f"Quiz {index}")
            question_ids.append(question_id)
        service = ReviewService(db._db_path)

        first_page = service.get_missed_questions_page(limit=2)
        second_page = service.get_missed_questions_page(limit=2, offset=2)
        final_page = service.get_missed_questions_page(limit=2, offset=4)

        assert service.count_missed_questions() == 5
        assert [item["question_id"] for item in first_page] == question_ids[:2]
        assert [item["question_id"] for item in second_page] == question_ids[2:4]
        assert [item["question_id"] for item in final_page] == question_ids[4:]

    def test_frequently_missed_pages_preserve_scope_and_thresholds(self, db):
        """Frequently missed pagination preserves existing filters."""
        first_test_id, first_question_id = _create_missed_test(db, "Quiz 1")
        second_test_id, second_question_id = _create_missed_test(db, "Quiz 2")
        _create_missed_test(db, "Quiz 3")
        service = ReviewService(db._db_path)

        page = service.get_frequently_missed_page(
            limit=10,
            test_ids=[first_test_id, second_test_id],
            min_attempts=2,
            miss_threshold=0.5,
        )
        total = service.count_frequently_missed(
            test_ids=[first_test_id, second_test_id],
            min_attempts=2,
            miss_threshold=0.5,
        )

        assert total == 2
        assert {item["question_id"] for item in page} == {
            first_question_id,
            second_question_id,
        }

    def test_empty_selected_scope_has_no_page_or_count(self, db_with_attempts):
        """An empty selected test scope does not return unrelated questions."""
        db, _ = db_with_attempts
        service = ReviewService(db._db_path)

        assert service.get_missed_questions_page(limit=50, test_ids=[]) == []
        assert service.count_missed_questions(test_ids=[]) == 0

    def test_full_list_and_page_queries_return_equivalent_rows(self, db_with_attempts):
        """Legacy and paged Review APIs share the same aggregate result set."""
        db, _ = db_with_attempts
        service = ReviewService(db._db_path)

        missed = service.get_missed_questions()
        missed_page = service.get_missed_questions_page(limit=50)
        frequent = service.get_frequently_missed(min_attempts=2, miss_threshold=0.5)
        frequent_page = service.get_frequently_missed_page(
            limit=50, min_attempts=2, miss_threshold=0.5
        )

        assert missed_page == missed
        assert frequent_page == frequent

    def test_paged_retrieval_rejects_conflicting_filters(self, db_with_attempts):
        """Paged Review retrieval keeps the existing filter contract."""
        db, test_id = db_with_attempts
        service = ReviewService(db._db_path)

        with pytest.raises(ValueError):
            service.get_missed_questions_page(limit=50, test_id=test_id, test_ids=[])
        with pytest.raises(ValueError):
            service.count_missed_questions(test_id=test_id, test_ids=[])


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

"""Tests for DatabaseManager."""

import pytest

from config.database import get_connection
from models.question import Question, QuestionOption
from models.test import Test
from models.test_result import QuestionResponse, TestAttempt


class TestDatabaseManagerTests:
    """Test CRUD operations."""

    def _save_attempt_at(
        self,
        db,
        test_id,
        completed_at,
        mode="test",
        score=1,
    ):
        """Save an attempt with a deterministic completion timestamp."""
        attempt_id = db.save_attempt(
            TestAttempt(
                test_id=test_id,
                score=score,
                total_questions=3,
                percentage=score / 3 * 100,
                mode=mode,
            )
        )
        conn = db._conn()
        try:
            conn.execute(
                "UPDATE test_attempts SET completed_at = ? WHERE id = ?",
                (completed_at, attempt_id),
            )
            conn.commit()
        finally:
            conn.close()
        return attempt_id

    def test_create_and_get_test(self, db):
        test = Test(name="My Test", description="Desc")
        test_id = db.create_test(test)
        assert test_id > 0

        fetched = db.get_test_by_id(test_id)
        assert fetched is not None
        assert fetched.name == "My Test"
        assert fetched.description == "Desc"

    def test_get_all_tests(self, db):
        db.create_test(Test(name="Test 1"))
        db.create_test(Test(name="Test 2"))
        tests = db.get_all_tests()
        assert len(tests) == 2

    def test_update_test(self, db):
        test_id = db.create_test(Test(name="Original"))
        test = db.get_test_by_id(test_id)
        test.name = "Updated"
        db.update_test(test)
        fetched = db.get_test_by_id(test_id)
        assert fetched.name == "Updated"

    def test_delete_test(self, db):
        test_id = db.create_test(Test(name="To Delete"))
        db.delete_test(test_id)
        assert db.get_test_by_id(test_id) is None

    def test_add_question_with_options(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q1?",
            type="multiple_choice",
            correct_answer="A",
            explanation="A is correct because it matches the prompt.",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)
        assert q_id > 0

        questions = db.get_questions_for_test(test_id)
        assert len(questions) == 1
        assert len(questions[0].options) == 2
        assert questions[0].options[0].is_correct is True
        assert questions[0].explanation == "A is correct because it matches the prompt."

    def test_load_questions_uses_one_joined_query_and_preserves_models(
        self, populated_db
    ):
        """Bulk test loading keeps question and option content in ID order."""
        db, test_id = populated_db
        conn = db._conn()
        statements = []
        conn.set_trace_callback(statements.append)
        original_conn = db._conn
        db._conn = lambda: conn
        try:
            questions = db.get_questions_for_test(test_id)
        finally:
            db._conn = original_conn

        assert [question.text for question in questions] == [
            "What is 2 + 2?",
            "What is the capital of France?",
            "Explain the theory of relativity.",
        ]
        assert [option.text for option in questions[0].options] == ["3", "4", "5", "6"]
        assert questions[2].options == []
        joined_queries = [
            statement
            for statement in statements
            if "LEFT JOIN question_options" in statement
        ]
        assert len(joined_queries) == 1

    def test_get_questions_for_attempt_returns_answered_questions_in_response_order(
        self, populated_db
    ):
        """Historical retrieval excludes unanswered questions and keeps options."""
        db, test_id = populated_db
        all_questions = db.get_questions_for_test(test_id)
        attempt_id = db.save_attempt(
            TestAttempt(test_id=test_id, score=1, total_questions=2, percentage=50.0)
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=all_questions[1].id,
                user_answer="Paris",
                is_correct=True,
            )
        )
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=all_questions[0].id,
                user_answer="3",
                is_correct=False,
                was_flagged=True,
            )
        )

        questions = db.get_questions_for_attempt(attempt_id)

        assert [question.id for question in questions] == [
            all_questions[1].id,
            all_questions[0].id,
        ]
        assert [option.text for option in questions[0].options] == [
            "London",
            "Paris",
            "Berlin",
        ]

    def test_get_questions_for_attempt_returns_empty_for_unknown_or_empty_attempt(
        self, populated_db
    ):
        """No-response attempts and unknown IDs do not require a full test load."""
        db, test_id = populated_db
        empty_attempt_id = db.save_attempt(
            TestAttempt(test_id=test_id, score=0, total_questions=0, percentage=0.0)
        )

        assert db.get_questions_for_attempt(empty_attempt_id) == []
        assert db.get_questions_for_attempt(999999) == []

    def test_update_question_explanation(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q?",
            type="multiple_choice",
            correct_answer="A",
            explanation="Original explanation.",
            options=[
                QuestionOption(text="A", is_correct=True),
                QuestionOption(text="B", is_correct=False),
            ],
        )
        q_id = db.add_question(q)

        q.id = q_id
        q.explanation = "Updated explanation."
        db.update_question(q)

        question = db.get_questions_for_test(test_id)[0]
        assert question.explanation == "Updated explanation."

    def test_delete_question_cascades_options(self, db):
        test_id = db.create_test(Test(name="T"))
        q = Question(
            test_id=test_id,
            text="Q?",
            type="multiple_choice",
            correct_answer="A",
            options=[QuestionOption(text="A", is_correct=True)],
        )
        q_id = db.add_question(q)
        db.delete_question(q_id)
        questions = db.get_questions_for_test(test_id)
        assert len(questions) == 0

    def test_get_question_count(self, populated_db):
        db, test_id = populated_db
        assert db.get_question_count(test_id) == 3

    def test_get_all_question_counts_includes_empty_and_populated_tests(
        self, populated_db
    ):
        """One grouped query reports zero and nonzero test question counts."""
        db, populated_test_id = populated_db
        empty_test_id = db.create_test(Test(name="Empty Test"))

        counts = db.get_all_question_counts()

        assert counts[populated_test_id] == 3
        assert counts[empty_test_id] == 0

    def test_save_and_get_attempt(self, populated_db):
        db, test_id = populated_db
        attempt = TestAttempt(
            test_id=test_id,
            score=2,
            total_questions=3,
            percentage=66.7,
            time_taken=120,
        )
        attempt_id = db.save_attempt(attempt)
        assert attempt_id > 0

        attempts = db.get_attempts_for_test(test_id)
        assert len(attempts) == 1
        assert attempts[0].score == 2

    def test_save_and_get_responses(self, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)

        attempt = TestAttempt(
            test_id=test_id, score=1, total_questions=3, percentage=50.0
        )
        attempt_id = db.save_attempt(attempt)

        resp = QuestionResponse(
            attempt_id=attempt_id,
            question_id=questions[0].id,
            user_answer="4",
            is_correct=True,
            was_flagged=False,
            time_spent=30,
        )
        db.save_response(resp)

        details = db.get_attempt_details(attempt_id)
        assert details is not None
        assert len(details.responses) == 1
        assert details.responses[0].is_correct is True

    def test_save_attempt_with_responses_is_atomic(self, populated_db):
        """A failed response insert must not leave a partial attempt behind."""
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        attempt = TestAttempt(
            test_id=test_id, score=1, total_questions=2, percentage=50.0
        )
        responses = [
            QuestionResponse(
                question_id=questions[0].id,
                user_answer="4",
                is_correct=True,
            ),
            QuestionResponse(
                question_id=999999,
                user_answer="invalid",
                is_correct=False,
            ),
        ]

        with pytest.raises(Exception):
            db.save_attempt_with_responses(attempt, responses)

        assert db.get_attempts_for_test(test_id) == []

    def test_save_attempt_with_responses_saves_all_responses(self, populated_db):
        """Bulk attempt saving preserves response data and response ownership."""
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        attempt = TestAttempt(
            test_id=test_id, score=1, total_questions=2, percentage=50.0
        )
        responses = [
            QuestionResponse(
                question_id=questions[0].id,
                user_answer="4",
                is_correct=True,
                was_flagged=True,
                time_spent=12,
            ),
            QuestionResponse(
                question_id=questions[1].id,
                user_answer="Rome",
                is_correct=False,
            ),
        ]

        attempt_id = db.save_attempt_with_responses(attempt, responses)
        details = db.get_attempt_details(attempt_id)

        assert len(details.responses) == 2
        assert all(response.attempt_id == attempt_id for response in responses)
        assert details.responses[0].was_flagged is True
        assert details.responses[0].time_spent == 12

    def test_get_test_statistics(self, populated_db):
        db, test_id = populated_db
        db.save_attempt(
            TestAttempt(test_id=test_id, score=2, total_questions=3, percentage=66.7)
        )
        db.save_attempt(
            TestAttempt(test_id=test_id, score=3, total_questions=3, percentage=100.0)
        )
        stats = db.get_test_statistics(test_id)
        assert stats["attempts"] == 2
        assert stats["best_score"] == 100.0

    def test_get_attempts_page_returns_newest_page(self, populated_db):
        """get_attempts_page returns only the requested newest attempts."""
        db, test_id = populated_db
        attempt_ids = [
            self._save_attempt_at(
                db,
                test_id,
                f"2026-01-01 10:0{index}:00",
                score=index + 1,
            )
            for index in range(5)
        ]

        page = db.get_attempts_page(limit=2)

        assert [attempt.id for attempt in page] == [attempt_ids[4], attempt_ids[3]]
        assert all(attempt.test_name == "Sample Test" for attempt in page)

    def test_get_attempts_page_offset_returns_next_page(self, populated_db):
        """get_attempts_page uses offset without overlapping prior rows."""
        db, test_id = populated_db
        attempt_ids = [
            self._save_attempt_at(
                db,
                test_id,
                f"2026-01-01 10:0{index}:00",
                score=index + 1,
            )
            for index in range(5)
        ]

        first_page = db.get_attempts_page(limit=2, offset=0)
        second_page = db.get_attempts_page(limit=2, offset=2)

        assert [attempt.id for attempt in first_page] == [
            attempt_ids[4],
            attempt_ids[3],
        ]
        assert [attempt.id for attempt in second_page] == [
            attempt_ids[2],
            attempt_ids[1],
        ]
        assert {attempt.id for attempt in first_page}.isdisjoint(
            {attempt.id for attempt in second_page}
        )

    def test_get_attempts_page_filters_by_test_and_mode(self, populated_db):
        """Paged attempt queries apply test and mode filters in SQL."""
        db, test_id = populated_db
        other_test_id = db.create_test(Test(name="Other Test"))
        self._save_attempt_at(
            db,
            test_id,
            "2026-01-01 10:00:00",
            mode="test",
        )
        practice_id = self._save_attempt_at(
            db,
            test_id,
            "2026-01-01 10:01:00",
            mode="practice",
        )
        self._save_attempt_at(
            db,
            other_test_id,
            "2026-01-01 10:02:00",
            mode="practice",
        )

        page = db.get_attempts_page(limit=10, test_id=test_id, mode="practice")

        assert [attempt.id for attempt in page] == [practice_id]
        assert page[0].test_id == test_id
        assert page[0].mode == "practice"

    def test_count_attempts_matches_filters(self, populated_db):
        """count_attempts uses the same filters as paged history loading."""
        db, test_id = populated_db
        other_test_id = db.create_test(Test(name="Other Test"))
        self._save_attempt_at(
            db,
            test_id,
            "2026-01-01 10:00:00",
            mode="test",
        )
        self._save_attempt_at(
            db,
            test_id,
            "2026-01-01 10:01:00",
            mode="practice",
        )
        self._save_attempt_at(
            db,
            other_test_id,
            "2026-01-01 10:02:00",
            mode="practice",
        )

        assert db.count_attempts() == 3
        assert db.count_attempts(test_id=test_id) == 2
        assert db.count_attempts(mode="practice") == 2
        assert db.count_attempts(test_id=test_id, mode="practice") == 1

    def test_delete_test_cascades_everything(self, populated_db):
        db, test_id = populated_db
        attempt_id = db.save_attempt(
            TestAttempt(test_id=test_id, score=1, total_questions=3, percentage=33.3)
        )
        questions = db.get_questions_for_test(test_id)
        db.save_response(
            QuestionResponse(
                attempt_id=attempt_id,
                question_id=questions[0].id,
                user_answer="4",
                is_correct=True,
            )
        )

        db.delete_test(test_id)
        assert db.get_test_by_id(test_id) is None
        assert db.get_questions_for_test(test_id) == []
        assert db.get_attempts_for_test(test_id) == []


class TestGetQuestionHistoryStats:
    """Tests for get_question_history_stats (used by weighted mix selection)."""

    def _insert_attempt(self, db_path, test_id, completed_at):
        conn = get_connection(db_path)
        try:
            cursor = conn.execute(
                "INSERT INTO test_attempts "
                "(test_id, score, total_questions, percentage, time_taken, "
                "mode, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (test_id, 0, 0, 0.0, 0, "test", completed_at),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    def test_empty_question_ids_returns_empty_dict(self, db):
        assert db.get_question_history_stats([]) == {}

    def test_unanswered_questions_get_defaults(self, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        qids = [q.id for q in questions]
        stats = db.get_question_history_stats(qids)
        assert set(stats.keys()) == set(qids)
        for qid in qids:
            assert stats[qid] == {
                "last_is_correct": None,
                "last_completed_at": None,
                "attempts_since": 0,
            }

    def test_tracks_last_response_and_attempts_since(self, db_path, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        q = questions[0]

        # Attempt 1 at 10:00 — answered correctly.
        a1 = self._insert_attempt(db_path, test_id, "2026-01-01 10:00:00")
        db.save_response(
            QuestionResponse(
                attempt_id=a1,
                question_id=q.id,
                user_answer="x",
                is_correct=True,
            )
        )

        # Two newer attempts (no response for q) at 10:01 and 10:02.
        self._insert_attempt(db_path, test_id, "2026-01-01 10:01:00")
        self._insert_attempt(db_path, test_id, "2026-01-01 10:02:00")

        stats = db.get_question_history_stats([q.id])
        assert stats[q.id]["last_is_correct"] is True
        assert stats[q.id]["last_completed_at"] == "2026-01-01 10:00:00"
        assert stats[q.id]["attempts_since"] == 2

    def test_essay_response_yields_none_is_correct(self, db_path, populated_db):
        db, test_id = populated_db
        questions = db.get_questions_for_test(test_id)
        essay = next(q for q in questions if q.type == "essay")

        a1 = self._insert_attempt(db_path, test_id, "2026-01-01 10:00:00")
        db.save_response(
            QuestionResponse(
                attempt_id=a1,
                question_id=essay.id,
                user_answer="my essay",
                is_correct=None,
            )
        )

        stats = db.get_question_history_stats([essay.id])
        assert stats[essay.id]["last_is_correct"] is None
        assert stats[essay.id]["last_completed_at"] == "2026-01-01 10:00:00"

    def test_chunks_large_question_id_lists(self, db):
        """Large candidate lists avoid SQLite's host-parameter limit."""
        question_ids = list(range(1, 1002))

        stats = db.get_question_history_stats(question_ids)

        assert set(stats) == set(question_ids)
        assert all(
            stat
            == {
                "last_is_correct": None,
                "last_completed_at": None,
                "attempts_since": 0,
            }
            for stat in stats.values()
        )

    def test_same_timestamp_uses_latest_attempt_response(self, db_path, populated_db):
        """Equal completion timestamps resolve to the newest saved response."""
        db, test_id = populated_db
        question = db.get_questions_for_test(test_id)[0]
        completed_at = "2026-01-01 10:00:00"

        first_attempt = self._insert_attempt(db_path, test_id, completed_at)
        db.save_response(
            QuestionResponse(
                attempt_id=first_attempt,
                question_id=question.id,
                user_answer="correct",
                is_correct=True,
            )
        )
        second_attempt = self._insert_attempt(db_path, test_id, completed_at)
        db.save_response(
            QuestionResponse(
                attempt_id=second_attempt,
                question_id=question.id,
                user_answer="incorrect",
                is_correct=False,
            )
        )

        stats = db.get_question_history_stats([question.id])

        assert stats[question.id] == {
            "last_is_correct": False,
            "last_completed_at": completed_at,
            "attempts_since": 0,
        }

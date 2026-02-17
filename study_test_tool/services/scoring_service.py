"""Scoring service for evaluating test attempts."""

from collections import defaultdict
from typing import Dict, List, Optional

from config.settings import QUESTION_TYPE_ESSAY, QUESTION_TYPE_MC
from database.db_manager import DatabaseManager
from models.question import Question
from models.test_result import QuestionResponse, TestAttempt


class ScoringService:
    """Scores test attempts and persists results."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    @staticmethod
    def score_question(question: Question, user_answer: Optional[str]) -> Optional[bool]:
        """Score a single question.

        Args:
            question: The question being answered.
            user_answer: The user's answer text.

        Returns:
            True if correct, False if incorrect, None for essay questions.
        """
        if question.type == QUESTION_TYPE_ESSAY:
            return None
        if not user_answer:
            return False
        return user_answer.strip() == question.correct_answer.strip()

    def score_test(self, session) -> Dict:
        """Score a completed test session.

        Args:
            session: A TestSession object with questions and responses.

        Returns:
            Dict with score, total, percentage, correct_questions,
            incorrect_questions, essay_questions, time_taken.
        """
        correct = 0
        incorrect = 0
        essays = 0
        scored_responses = []

        for question in session.questions:
            user_answer = session.responses.get(question.id)
            is_correct = self.score_question(question, user_answer)

            if is_correct is None:
                essays += 1
            elif is_correct:
                correct += 1
            else:
                incorrect += 1

            scored_responses.append(
                QuestionResponse(
                    question_id=question.id,
                    user_answer=user_answer,
                    is_correct=is_correct,
                    was_flagged=question.id in session.flagged,
                    time_spent=session.question_times.get(question.id),
                )
            )

        mc_total = correct + incorrect
        percentage = (correct / mc_total * 100) if mc_total > 0 else 0.0
        time_taken = session.get_elapsed_time()

        return {
            "score": correct,
            "total": mc_total,
            "total_questions": len(session.questions),
            "percentage": round(percentage, 1),
            "correct_questions": correct,
            "incorrect_questions": incorrect,
            "essay_questions": essays,
            "time_taken": time_taken,
            "responses": scored_responses,
        }

    def save_attempt(
        self, test_id: int, score_data: Dict, mode: str = "test"
    ) -> int:
        """Persist a test attempt and its responses to the database.

        Args:
            test_id: The test that was taken.
            score_data: The dict returned by score_test().
            mode: "test" or "practice".

        Returns:
            The id of the saved test attempt.
        """
        attempt = TestAttempt(
            test_id=test_id,
            score=score_data["score"],
            total_questions=score_data["total_questions"],
            percentage=score_data["percentage"],
            time_taken=score_data["time_taken"],
            mode=mode,
        )
        attempt_id = self._db.save_attempt(attempt)

        for response in score_data["responses"]:
            response.attempt_id = attempt_id
            self._db.save_response(response)

        return attempt_id

    def save_mixed_attempt(
        self,
        score_data: Dict,
        questions: list,
        mode: str = "test",
    ) -> List[int]:
        """Save a mix test as separate per-source-test attempts.

        Groups responses by their originating test_id and saves one attempt
        per source test so analytics track back to each original test.

        Args:
            score_data: The dict returned by score_test().
            questions: The list of Question objects from the session.
            mode: "test" or "practice".

        Returns:
            List of saved attempt IDs.
        """
        # Build question_id → test_id lookup
        qid_to_test: Dict[int, int] = {}
        for q in questions:
            if q.test_id is not None:
                qid_to_test[q.id] = q.test_id

        # Group responses by source test
        grouped: Dict[int, List[QuestionResponse]] = defaultdict(list)
        for response in score_data["responses"]:
            source_test_id = qid_to_test.get(response.question_id)
            if source_test_id is not None:
                grouped[source_test_id].append(response)

        total_time = score_data.get("time_taken", 0)
        total_questions = len(score_data["responses"])

        attempt_ids: List[int] = []
        for test_id, responses in grouped.items():
            correct = sum(1 for r in responses if r.is_correct is True)
            incorrect = sum(1 for r in responses if r.is_correct is False)
            essays = sum(1 for r in responses if r.is_correct is None)
            mc_total = correct + incorrect
            percentage = (correct / mc_total * 100) if mc_total > 0 else 0.0

            # Proportional time allocation
            proportion = len(responses) / total_questions if total_questions > 0 else 0
            proportional_time = int(total_time * proportion)

            per_test_score_data = {
                "score": correct,
                "total": mc_total,
                "total_questions": len(responses),
                "percentage": round(percentage, 1),
                "correct_questions": correct,
                "incorrect_questions": incorrect,
                "essay_questions": essays,
                "time_taken": proportional_time,
                "responses": responses,
            }

            attempt_id = self.save_attempt(test_id, per_test_score_data, mode)
            attempt_ids.append(attempt_id)

        return attempt_ids

    def get_attempt_details(self, attempt_id: int) -> Optional[TestAttempt]:
        """Load a saved attempt with all responses."""
        return self._db.get_attempt_details(attempt_id)

    def get_all_attempts(self):
        """Get all test attempts."""
        return self._db.get_all_attempts()

    def get_attempts_for_test(self, test_id: int):
        """Get all attempts for a specific test."""
        return self._db.get_attempts_for_test(test_id)

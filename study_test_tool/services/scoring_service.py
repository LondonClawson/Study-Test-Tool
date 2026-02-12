"""Scoring service for evaluating test attempts."""

from typing import Dict, Optional

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

    def save_attempt(self, test_id: int, score_data: Dict) -> int:
        """Persist a test attempt and its responses to the database.

        Args:
            test_id: The test that was taken.
            score_data: The dict returned by score_test().

        Returns:
            The id of the saved test attempt.
        """
        attempt = TestAttempt(
            test_id=test_id,
            score=score_data["score"],
            total_questions=score_data["total_questions"],
            percentage=score_data["percentage"],
            time_taken=score_data["time_taken"],
        )
        attempt_id = self._db.save_attempt(attempt)

        for response in score_data["responses"]:
            response.attempt_id = attempt_id
            self._db.save_response(response)

        return attempt_id

    def get_attempt_details(self, attempt_id: int) -> Optional[TestAttempt]:
        """Load a saved attempt with all responses."""
        return self._db.get_attempt_details(attempt_id)

    def get_all_attempts(self):
        """Get all test attempts."""
        return self._db.get_all_attempts()

    def get_attempts_for_test(self, test_id: int):
        """Get all attempts for a specific test."""
        return self._db.get_attempts_for_test(test_id)

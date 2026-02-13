"""Review service for missed questions analysis."""

from typing import Dict, List, Optional

from database.db_manager import DatabaseManager
from models.question import Question


class ReviewService:
    """Business logic for missed questions review."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    def get_missed_questions(
        self, test_id: Optional[int] = None
    ) -> List[Dict]:
        """Get all questions that have been missed at least once.

        Args:
            test_id: Optional filter by test.

        Returns:
            List of dicts with question info and miss statistics.
        """
        return self._db.get_missed_questions(test_id)

    def get_frequently_missed(
        self,
        test_id: Optional[int] = None,
        min_attempts: int = 3,
        miss_threshold: float = 0.5,
    ) -> List[Dict]:
        """Get questions that are frequently answered incorrectly.

        Args:
            test_id: Optional filter by test.
            min_attempts: Minimum number of attempts to consider.
            miss_threshold: Minimum miss rate (0.0-1.0) to qualify.

        Returns:
            Filtered list of frequently missed question dicts.
        """
        return self._db.get_frequently_missed_questions(
            test_id, min_attempts, miss_threshold
        )

    def create_review_session_questions(
        self, question_ids: List[int]
    ) -> List[Question]:
        """Load full Question objects for a review session.

        Args:
            question_ids: List of question IDs to load.

        Returns:
            List of Question objects with options.
        """
        questions = []
        for qid in question_ids:
            question = self._db.get_question_by_id(qid)
            if question:
                questions.append(question)
        return questions

"""Question management service."""

from typing import List, Optional

from database.db_manager import DatabaseManager
from models.question import Question, QuestionOption
from services.randomizer_service import RandomizerService


class QuestionService:
    """Business logic for question CRUD and retrieval."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    def get_questions_for_test(
        self, test_id: int, randomize: bool = False
    ) -> List[Question]:
        """Get all questions for a test, optionally randomized.

        Args:
            test_id: The test to fetch questions for.
            randomize: If True, shuffle question order and option order.

        Returns:
            List of Question objects with options loaded.
        """
        questions = self._db.get_questions_for_test(test_id)
        if randomize:
            questions = RandomizerService.shuffle_all(questions)
        return questions

    def add_question(self, question: Question) -> int:
        """Add a question with its options and return its id."""
        return self._db.add_question(question)

    def update_question(self, question: Question) -> None:
        """Update a question's text, type, correct_answer, and category.

        Also replaces all options: deletes existing, inserts new ones.
        """
        self._db.update_question(question)
        self._db.delete_options_for_question(question.id)
        for option in question.options:
            option.question_id = question.id
            self._db.add_question_option(option)

    def delete_question(self, question_id: int) -> None:
        """Delete a question and its options."""
        self._db.delete_question(question_id)

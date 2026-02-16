"""Export service for saving tests to JSON files."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from config.settings import QUESTION_TYPE_ESSAY, QUESTION_TYPE_MC
from database.db_manager import DatabaseManager
from models.question import Question
from models.test import Test


class ExportService:
    """Handles exporting tests to JSON files."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    def export_to_json(self, test_id: int, file_path: str) -> None:
        """Export a test to a JSON file.

        Args:
            test_id: The id of the test to export.
            file_path: Destination path for the JSON file.

        Raises:
            ValueError: If the test does not exist.
        """
        test = self._db.get_test_by_id(test_id)
        if test is None:
            raise ValueError(f"Test with id {test_id} not found.")

        data = self._test_to_dict(test)

        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def validate_test(self, test_id: int) -> List[str]:
        """Check a test for problems and return warning strings.

        Returns:
            A list of warning messages. Empty list means no issues.
        """
        test = self._db.get_test_by_id(test_id)
        if test is None:
            raise ValueError(f"Test with id {test_id} not found.")

        warnings: List[str] = []
        for i, question in enumerate(test.questions, start=1):
            if question.type == QUESTION_TYPE_MC:
                if not question.correct_answer:
                    warnings.append(
                        f"Q{i} has no correct answer set."
                    )
                if not question.options:
                    warnings.append(f"Q{i} has no answer options.")
            elif question.type == QUESTION_TYPE_ESSAY:
                if not question.correct_answer:
                    warnings.append(
                        f"Q{i} (essay) has no expected answer set."
                    )
        return warnings

    @staticmethod
    def _test_to_dict(test: Test) -> Dict:
        """Convert a Test object to the standard JSON import/export dict."""
        questions = []
        for q in test.questions:
            q_dict: Dict = {
                "text": q.text,
                "type": q.type,
            }
            if q.category:
                q_dict["category"] = q.category

            if q.type == QUESTION_TYPE_MC:
                q_dict["options"] = [
                    {"text": opt.text, "correct": opt.is_correct}
                    for opt in q.options
                ]
            elif q.type == QUESTION_TYPE_ESSAY:
                q_dict["expected_answer"] = q.correct_answer

            questions.append(q_dict)

        data: Dict = {
            "name": test.name,
            "description": test.description,
            "questions": questions,
        }
        return data

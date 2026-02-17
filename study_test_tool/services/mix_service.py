"""Mix test service — selects random questions from multiple tests."""

import random
from typing import List, Optional

from models.question import Question
from services.question_service import QuestionService
from services.randomizer_service import RandomizerService


class MixService:
    """Loads questions from multiple tests and randomly selects a subset."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._question_service = QuestionService(db_path)

    def select_questions(
        self,
        test_ids: List[int],
        count: int,
        randomize: bool = True,
    ) -> List[Question]:
        """Select a random subset of questions from multiple tests.

        Args:
            test_ids: IDs of the tests to draw questions from.
            count: Number of questions to select.
            randomize: If True, shuffle question and option order.

        Returns:
            List of Question objects, each retaining its original test_id.
        """
        if not test_ids or count <= 0:
            return []

        all_questions: List[Question] = []
        for test_id in test_ids:
            questions = self._question_service.get_questions_for_test(
                test_id, randomize=False
            )
            all_questions.extend(questions)

        if not all_questions:
            return []

        selected = random.sample(all_questions, min(count, len(all_questions)))

        if randomize:
            selected = RandomizerService.shuffle_all(selected)

        return selected

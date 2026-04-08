"""Mix test service — selects weighted-random questions from multiple tests."""

import random
from typing import Dict, List, Optional

from database.db_manager import DatabaseManager
from models.question import Question
from services.question_service import QuestionService
from services.randomizer_service import RandomizerService

# History-based weighting constants. Unseen and last-incorrect questions keep
# weight 1.0; questions whose most recent response was correct are penalized
# and recover linearly toward 1.0 over RECOVERY_ATTEMPTS subsequent attempts.
WEIGHT_FLOOR: float = 0.1
RECOVERY_ATTEMPTS: int = 5


def _compute_weight(stats: Dict) -> float:
    """Weight a question based on its history stats.

    - Never answered, essay response (is_correct None), or last answer wrong → 1.0
    - Last answer correct → WEIGHT_FLOOR + (1 - WEIGHT_FLOOR) * min(1, k / RECOVERY)
      where k is the number of test_attempts completed since that response.
    """
    last = stats["last_is_correct"]
    if last is None or last is False:
        return 1.0
    k = stats["attempts_since"]
    progress = min(1.0, k / RECOVERY_ATTEMPTS)
    return WEIGHT_FLOOR + (1.0 - WEIGHT_FLOOR) * progress


def _weighted_sample_without_replacement(
    items: List[Question], weights: List[float], k: int
) -> List[Question]:
    """Efraimidis–Spirakis weighted reservoir sampling (pure stdlib).

    Assigns each item a key ``random() ** (1 / weight)`` and returns the top-k
    items by key. Equivalent to weighted sampling without replacement.
    """
    if k <= 0 or not items:
        return []
    keyed = []
    for item, w in zip(items, weights):
        w = max(w, 1e-9)
        key = random.random() ** (1.0 / w)
        keyed.append((key, item))
    keyed.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in keyed[:k]]


class MixService:
    """Loads questions from multiple tests and selects a weighted subset."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._question_service = QuestionService(db_path)
        self._db = DatabaseManager(db_path)

    def select_questions(
        self,
        test_ids: List[int],
        count: int,
        randomize: bool = True,
    ) -> List[Question]:
        """Select a history-weighted subset of questions from multiple tests.

        Questions the user has never seen or answered incorrectly most recently
        are preferred. Questions answered correctly most recently are penalized
        and recover over subsequent attempts.

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

        question_ids = [q.id for q in all_questions if q.id is not None]
        history = self._db.get_question_history_stats(question_ids)
        weights = [
            _compute_weight(
                history.get(
                    q.id,
                    {
                        "last_is_correct": None,
                        "last_completed_at": None,
                        "attempts_since": 0,
                    },
                )
            )
            for q in all_questions
        ]

        k = min(count, len(all_questions))
        selected = _weighted_sample_without_replacement(all_questions, weights, k)

        if randomize:
            selected = RandomizerService.shuffle_all(selected)

        return selected

"""Test session — tracks state during test-taking."""

import time
from typing import Dict, List, Optional, Set

from models.question import Question


class TestSession:
    """Manages the state of an active test-taking session."""

    def __init__(
        self,
        test_id: Optional[int],
        questions: List[Question],
        mode: str = "test",
    ) -> None:
        self.test_id: Optional[int] = test_id
        self.questions: List[Question] = questions
        self.mode: str = mode
        self.current_index: int = 0
        self.responses: Dict[int, str] = {}  # question_id → answer text
        self.flagged: Set[int] = set()  # question_ids
        self.question_times: Dict[int, int] = {}  # question_id → seconds
        self._start_time: float = 0.0
        self._question_start_time: float = 0.0

    def start(self) -> None:
        """Start the test session and begin timing."""
        self._start_time = time.time()
        self._question_start_time = time.time()

    def get_current_question(self) -> Optional[Question]:
        """Get the current question."""
        if 0 <= self.current_index < len(self.questions):
            return self.questions[self.current_index]
        return None

    def save_response(self, question_id: int, answer: str) -> None:
        """Save or update a response for a question."""
        if answer:
            self.responses[question_id] = answer
        elif question_id in self.responses:
            del self.responses[question_id]

    def flag_question(self, question_id: int) -> bool:
        """Toggle the flagged status of a question.

        Returns:
            True if now flagged, False if unflagged.
        """
        if question_id in self.flagged:
            self.flagged.discard(question_id)
            return False
        self.flagged.add(question_id)
        return True

    def _record_question_time(self) -> None:
        """Record time spent on the current question."""
        if self._question_start_time > 0:
            question = self.get_current_question()
            if question:
                elapsed = int(time.time() - self._question_start_time)
                existing = self.question_times.get(question.id, 0)
                self.question_times[question.id] = existing + elapsed
        self._question_start_time = time.time()

    def next_question(self) -> Optional[Question]:
        """Move to the next question. Returns it, or None if at the end."""
        self._record_question_time()
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            return self.get_current_question()
        return None

    def previous_question(self) -> Optional[Question]:
        """Move to the previous question. Returns it, or None if at start."""
        self._record_question_time()
        if self.current_index > 0:
            self.current_index -= 1
            return self.get_current_question()
        return None

    def go_to_question(self, index: int) -> Optional[Question]:
        """Jump to a specific question by index."""
        self._record_question_time()
        if 0 <= index < len(self.questions):
            self.current_index = index
            return self.get_current_question()
        return None

    def finish_test(self) -> None:
        """Finalize the session, recording the last question's time."""
        self._record_question_time()

    def get_elapsed_time(self) -> int:
        """Get total elapsed time in seconds since start."""
        if self._start_time > 0:
            return int(time.time() - self._start_time)
        return 0

    def get_unanswered_count(self) -> int:
        """Get the number of unanswered questions."""
        return len(self.questions) - len(self.responses)

    def get_flagged_count(self) -> int:
        """Get the number of flagged questions."""
        return len(self.flagged)

    @property
    def total_questions(self) -> int:
        """Total number of questions in the session."""
        return len(self.questions)

    @property
    def is_question_answered(self) -> bool:
        """Whether the current question has been answered."""
        question = self.get_current_question()
        return question is not None and question.id in self.responses

    @property
    def is_mix_test(self) -> bool:
        """Whether this session is a mix test (questions from multiple tests)."""
        return self.test_id is None

    @property
    def is_question_flagged(self) -> bool:
        """Whether the current question is flagged."""
        question = self.get_current_question()
        return question is not None and question.id in self.flagged

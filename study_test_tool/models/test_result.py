"""Test attempt and question response data models."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QuestionResponse:
    """Represents a user's response to a single question during a test attempt."""

    question_id: int
    user_answer: Optional[str] = None
    is_correct: Optional[bool] = None  # None for essay questions
    was_flagged: bool = False
    time_spent: Optional[int] = None  # seconds
    id: Optional[int] = None
    attempt_id: Optional[int] = None


@dataclass
class TestAttempt:
    """Represents a completed test attempt with score and responses."""

    test_id: int
    score: int = 0
    total_questions: int = 0
    percentage: float = 0.0
    time_taken: Optional[int] = None  # seconds
    mode: str = "test"  # "test" or "practice"
    completed_at: Optional[str] = None
    id: Optional[int] = None
    test_name: Optional[str] = None  # populated via JOIN for display
    responses: List[QuestionResponse] = field(default_factory=list)

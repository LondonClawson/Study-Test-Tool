"""Question and QuestionOption data models."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class QuestionOption:
    """Represents a single option for a multiple-choice question."""

    text: str
    is_correct: bool = False
    id: Optional[int] = None
    question_id: Optional[int] = None


@dataclass
class Question:
    """Represents a test question (multiple-choice or essay)."""

    text: str
    type: str  # 'multiple_choice' or 'essay'
    correct_answer: str = ""
    category: str = ""
    id: Optional[int] = None
    test_id: Optional[int] = None
    options: List[QuestionOption] = field(default_factory=list)
    created_at: Optional[str] = None

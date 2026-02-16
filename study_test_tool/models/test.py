"""Test data model."""

from dataclasses import dataclass, field
from typing import List, Optional

from models.question import Question


@dataclass
class Test:
    """Represents a test containing questions."""

    name: str
    description: str = ""
    group_name: str = ""
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    questions: List[Question] = field(default_factory=list)

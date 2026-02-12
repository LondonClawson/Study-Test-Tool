"""Input validation utilities."""

from typing import List, Optional

from config.settings import QUESTION_TYPE_ESSAY, QUESTION_TYPE_MC


def validate_test_name(name: str) -> Optional[str]:
    """Validate a test name. Returns error message or None if valid."""
    name = name.strip()
    if not name:
        return "Test name is required."
    if len(name) > 200:
        return "Test name must be 200 characters or less."
    return None


def validate_question_text(text: str) -> Optional[str]:
    """Validate question text. Returns error message or None if valid."""
    text = text.strip()
    if not text:
        return "Question text is required."
    return None


def validate_mc_options(options: List[dict]) -> Optional[str]:
    """Validate multiple-choice options.

    Args:
        options: List of dicts with 'text' and 'is_correct' keys.

    Returns:
        Error message or None if valid.
    """
    non_empty = [o for o in options if o.get("text", "").strip()]
    if len(non_empty) < 2:
        return "At least 2 options are required."
    correct_count = sum(1 for o in non_empty if o.get("is_correct"))
    if correct_count == 0:
        return "One option must be marked as correct."
    if correct_count > 1:
        return "Only one option can be marked as correct."
    return None


def validate_question_type(question_type: str) -> Optional[str]:
    """Validate question type. Returns error message or None if valid."""
    if question_type not in (QUESTION_TYPE_MC, QUESTION_TYPE_ESSAY):
        return f"Invalid question type: {question_type}"
    return None

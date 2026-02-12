"""Import service for loading tests from JSON and text files."""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from config.settings import QUESTION_TYPE_ESSAY, QUESTION_TYPE_MC
from database.db_manager import DatabaseManager
from models.question import Question, QuestionOption
from models.test import Test


class ImportService:
    """Handles importing tests from JSON and plain-text files."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)

    # ── JSON Import ────────────────────────────────────────────

    def import_from_json(self, file_path: str) -> int:
        """Import a test from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            The id of the created test.

        Raises:
            ValueError: If the JSON format is invalid.
            FileNotFoundError: If the file doesn't exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._validate_json_format(data)

        test = Test(
            name=data.get("name", path.stem),
            description=data.get("description", ""),
        )
        test_id = self._db.create_test(test)

        for q_data in data.get("questions", []):
            question = self._parse_json_question(q_data, test_id)
            self._db.add_question(question)

        return test_id

    @staticmethod
    def _validate_json_format(data: Dict) -> None:
        """Validate the structure of imported JSON data."""
        if not isinstance(data, dict):
            raise ValueError("JSON root must be an object.")
        if "questions" not in data:
            raise ValueError("JSON must contain a 'questions' array.")
        if not isinstance(data["questions"], list):
            raise ValueError("'questions' must be an array.")
        if len(data["questions"]) == 0:
            raise ValueError("Test must contain at least one question.")

    @staticmethod
    def _parse_json_question(q_data: Dict, test_id: int) -> Question:
        """Parse a single question from JSON data."""
        q_type = q_data.get("type", QUESTION_TYPE_MC)
        text = q_data.get("text", "").strip()
        if not text:
            raise ValueError("Question text is required.")

        options = []
        correct_answer = ""

        if q_type == QUESTION_TYPE_MC:
            for o_data in q_data.get("options", []):
                opt = QuestionOption(
                    text=o_data.get("text", "").strip(),
                    is_correct=o_data.get("correct", False),
                )
                options.append(opt)
                if opt.is_correct:
                    correct_answer = opt.text
        elif q_type == QUESTION_TYPE_ESSAY:
            correct_answer = q_data.get("expected_answer", "").strip()

        return Question(
            test_id=test_id,
            text=text,
            type=q_type,
            correct_answer=correct_answer,
            category=q_data.get("category", ""),
            options=options,
        )

    # ── Text Import ────────────────────────────────────────────

    def import_from_text(self, file_path: str, test_name: Optional[str] = None) -> int:
        """Import a test from a plain-text file (test.txt format).

        Format expected:
            1. Question text
            a. Option A -- correct
            b. Option B
            ...

        Args:
            file_path: Path to the text file.
            test_name: Optional name for the test. Defaults to filename.

        Returns:
            The id of the created test.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")
        name = test_name if test_name else path.stem

        test = Test(name=name, description=f"Imported from {path.name}")
        test_id = self._db.create_test(test)

        questions = self._parse_text_questions(content)
        if not questions:
            raise ValueError("No questions found in the text file.")

        for question in questions:
            question.test_id = test_id
            self._db.add_question(question)

        return test_id

    def _parse_text_questions(self, content: str) -> List[Question]:
        """Parse questions from plain-text content."""
        # Split into question blocks by number prefix: "1." or "1)"
        # Handle case where number may start after blank lines
        blocks = re.split(r"(?:^|\n)(?=\d+\s*[.)]\s)", content.strip())
        blocks = [b.strip() for b in blocks if b.strip()]

        questions = []
        for block in blocks:
            question = self._parse_text_question_block(block)
            if question:
                questions.append(question)

        return questions

    def _parse_text_question_block(self, block: str) -> Optional[Question]:
        """Parse a single question block from text."""
        # Remove the leading number: "1. " or "1) "
        block = re.sub(r"^\d+\s*[.)]\s*", "", block, count=1)

        # Split into question text and options
        # Options start with a/b/c/d followed by . or )
        option_pattern = re.compile(
            r"^([a-dA-D])\s*[.)]\s*(.*?)$", re.MULTILINE
        )
        option_matches = list(option_pattern.finditer(block))

        if not option_matches:
            return None

        # Question text is everything before the first option
        question_text = block[: option_matches[0].start()].strip()
        if not question_text:
            return None

        # Parse options — handle multi-line options and correct markers
        options = []
        correct_answer = ""

        for i, match in enumerate(option_matches):
            # Get option text: from after the letter prefix to the next option
            # or end of block
            start = match.end()
            end = option_matches[i + 1].start() if i + 1 < len(option_matches) else len(block)
            raw_text = match.group(2) + block[start:end]

            # Clean up: join lines, collapse whitespace
            raw_text = " ".join(raw_text.split())

            # Check for correct-answer marker
            is_correct, clean_text = self._extract_correct_marker(raw_text)

            # Handle garbled options (e.g., Q3 option b containing c's text)
            # If an option contains another option marker pattern mid-text,
            # truncate at that point
            next_option_in_text = re.search(
                r"\s+[☑]+\s+[A-Za-z]", clean_text
            )
            if next_option_in_text:
                clean_text = clean_text[: next_option_in_text.start()].strip()

            if clean_text:
                opt = QuestionOption(text=clean_text, is_correct=is_correct)
                options.append(opt)
                if is_correct:
                    correct_answer = clean_text

        # If multiple marked correct (e.g., Q5), resolve:
        # prefer "-- correct" over other markers
        correct_opts = [o for o in options if o.is_correct]
        if len(correct_opts) > 1:
            # Keep only the one with the strongest marker (handled in extract)
            # As a fallback, keep the last one marked
            for opt in options:
                opt.is_correct = False
            correct_opts[-1].is_correct = True
            correct_answer = correct_opts[-1].text

        if not options:
            return None

        return Question(
            text=question_text,
            type=QUESTION_TYPE_MC,
            correct_answer=correct_answer,
            options=options,
        )

    @staticmethod
    def _extract_correct_marker(text: str) -> tuple:
        """Extract correct-answer marker from option text.

        Returns:
            Tuple of (is_correct: bool, cleaned_text: str)
        """
        # Pattern: -- correct  or  --correct
        correct_pattern = re.compile(r"\s*--\s*correct\s*$", re.IGNORECASE)
        if correct_pattern.search(text):
            clean = correct_pattern.sub("", text).strip()
            return True, clean

        # Pattern: --already established (or similar)
        established_pattern = re.compile(
            r"\s*--\s*already\s+establish\w*\s*$", re.IGNORECASE
        )
        if established_pattern.search(text):
            clean = established_pattern.sub("", text).strip()
            return True, clean

        return False, text.strip()

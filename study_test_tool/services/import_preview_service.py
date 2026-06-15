"""Preview and validation helpers for test imports."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from config.settings import QUESTION_TYPE_MC
from models.question import Question


@dataclass
class ImportPreview:
    """Parsed import data waiting for user confirmation."""

    source_name: str
    test_name: str
    description: str
    group_name: str
    question_count: int
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    payload: Optional[Dict[str, Any]] = None


class ImportPreviewService:
    """Build import previews and validate import payloads."""

    def preview_from_dict(
        self,
        data: Dict,
        fallback_name: str = "",
        source_name: str = "",
    ) -> ImportPreview:
        """Build an import preview from an already-parsed payload dict."""
        self.validate_json_format(data)
        test_name = data.get("name") or fallback_name
        payload = dict(data)
        payload["name"] = test_name
        payload.setdefault("description", "")
        payload.setdefault("group_name", "")

        errors, warnings = self.validate_payload_questions(payload)
        question_count = len(payload.get("questions", []))
        if question_count < 3:
            warnings.append(f"Only {question_count} question(s) were detected.")

        return ImportPreview(
            source_name=source_name or test_name,
            test_name=test_name,
            description=payload.get("description", ""),
            group_name=payload.get("group_name", ""),
            question_count=question_count,
            warnings=warnings,
            errors=errors,
            payload=payload,
        )

    @staticmethod
    def validate_json_format(data: Dict) -> None:
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
    def question_to_payload(question: Question) -> Dict[str, Any]:
        """Convert a parsed text question to the JSON import contract."""
        return {
            "text": question.text,
            "type": question.type,
            "category": question.category,
            "explanation": question.explanation,
            "expected_answer": question.correct_answer,
            "options": [
                {"text": option.text, "correct": option.is_correct}
                for option in question.options
            ],
        }

    @staticmethod
    def validate_payload_questions(payload: Dict) -> tuple[List[str], List[str]]:
        """Return blocking errors and non-blocking warnings for a payload."""
        errors: List[str] = []
        warnings: List[str] = []

        for index, q_data in enumerate(payload.get("questions", []), start=1):
            text = q_data.get("text", "").strip()
            if not text:
                errors.append(f"Question {index} is missing text.")
            elif len(text) > 2000:
                warnings.append(f"Question {index} has unusually long text.")

            q_type = q_data.get("type", QUESTION_TYPE_MC)
            if q_type == QUESTION_TYPE_MC:
                options = q_data.get("options", [])
                if not options:
                    errors.append(f"Question {index} has no answer options.")
                    continue

                correct_count = 0
                for opt_index, option in enumerate(options, start=1):
                    option_text = option.get("text", "").strip()
                    if not option_text:
                        errors.append(
                            f"Question {index} option {opt_index} is missing text."
                        )
                    elif len(option_text) > 1000:
                        warnings.append(
                            f"Question {index} option {opt_index} is unusually long."
                        )
                    if option.get("correct", False):
                        correct_count += 1

                if correct_count == 0:
                    errors.append(f"Question {index} has no correct answer set.")
                elif correct_count > 1:
                    errors.append(f"Question {index} has multiple correct answers set.")

        return errors, warnings

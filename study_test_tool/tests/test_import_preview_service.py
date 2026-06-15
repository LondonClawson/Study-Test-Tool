"""Tests for import preview construction and validation."""

from models.question import Question, QuestionOption
from services.import_preview_service import ImportPreviewService


def test_preview_from_dict_does_not_require_database():
    svc = ImportPreviewService()
    data = {
        "name": "Preview Test",
        "questions": [
            {
                "text": "Q?",
                "type": "multiple_choice",
                "options": [
                    {"text": "A", "correct": True},
                    {"text": "B", "correct": False},
                ],
            }
        ],
    }

    preview = svc.preview_from_dict(data)

    assert preview.test_name == "Preview Test"
    assert preview.question_count == 1
    assert preview.payload["description"] == ""
    assert preview.payload["group_name"] == ""


def test_preview_preserves_source_group_name():
    svc = ImportPreviewService()
    preview = svc.preview_from_dict(
        {
            "name": "Grouped",
            "group_name": "Contracts",
            "questions": [
                {
                    "text": "Q?",
                    "type": "multiple_choice",
                    "options": [
                        {"text": "A", "correct": True},
                        {"text": "B", "correct": False},
                    ],
                }
            ],
        }
    )

    assert preview.group_name == "Contracts"
    assert preview.payload["group_name"] == "Contracts"


def test_preview_blocks_missing_correct_answer():
    svc = ImportPreviewService()
    preview = svc.preview_from_dict(
        {
            "name": "Invalid Preview",
            "questions": [
                {
                    "text": "Q?",
                    "type": "multiple_choice",
                    "options": [
                        {"text": "A", "correct": False},
                        {"text": "B", "correct": False},
                    ],
                }
            ],
        }
    )

    assert preview.errors == ["Question 1 has no correct answer set."]


def test_question_to_payload_preserves_question_fields():
    svc = ImportPreviewService()
    question = Question(
        text="Q?",
        type="multiple_choice",
        category="Law",
        explanation="Because.",
        correct_answer="A",
        options=[
            QuestionOption(text="A", is_correct=True),
            QuestionOption(text="B", is_correct=False),
        ],
    )

    payload = svc.question_to_payload(question)

    assert payload["text"] == "Q?"
    assert payload["category"] == "Law"
    assert payload["explanation"] == "Because."
    assert payload["options"][0] == {"text": "A", "correct": True}

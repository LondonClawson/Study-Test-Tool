"""Tests for ImportService."""

import json
import os
import tempfile

import pytest

from config.database import initialize_database
from models.question import Question, QuestionOption
from services.import_service import ImportService


@pytest.fixture
def import_svc():
    """ImportService backed by a temporary SQLite file."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    initialize_database(path)
    yield ImportService(path)
    os.unlink(path)


class TestJsonImport:
    """Test JSON import functionality."""

    def test_import_valid_json(self, import_svc):
        data = {
            "name": "JSON Test",
            "description": "A test",
            "questions": [
                {
                    "text": "What is 1+1?",
                    "type": "multiple_choice",
                    "category": "Math",
                    "options": [
                        {"text": "1", "correct": False},
                        {"text": "2", "correct": True},
                    ],
                }
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        try:
            test_id = import_svc.import_from_json(path)
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_json_missing_questions(self, import_svc):
        data = {"name": "Bad Test"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        try:
            with pytest.raises(ValueError, match="questions"):
                import_svc.import_from_json(path)
        finally:
            os.unlink(path)

    def test_import_json_empty_questions(self, import_svc):
        data = {"name": "Empty", "questions": []}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        try:
            with pytest.raises(ValueError, match="at least one"):
                import_svc.import_from_json(path)
        finally:
            os.unlink(path)

    def test_import_file_not_found(self, import_svc):
        with pytest.raises(FileNotFoundError):
            import_svc.import_from_json("/nonexistent/file.json")

    def test_import_from_dict_success(self, import_svc):
        """In-memory payload path used by the PDF import flow."""
        data = {
            "name": "Dict Test",
            "description": "In-memory",
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
        test_id = import_svc.import_from_dict(data)
        assert test_id > 0

    def test_import_service_preview_from_dict_does_not_write(self, import_svc):
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

        preview = import_svc.preview_from_dict(data)

        assert preview.test_name == "Preview Test"
        assert preview.question_count == 1
        assert not import_svc._db.get_all_tests()

    def test_commit_preview_applies_group_override(self, import_svc):
        data = {
            "name": "Grouped Preview",
            "group_name": "Original",
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

        preview = import_svc.preview_from_dict(data)
        test_id = import_svc.commit_preview(preview, group_name_override="Contracts")
        imported = import_svc._db.get_test_by_id(test_id)

        assert imported.group_name == "Contracts"

    def test_commit_preview_rejects_preview_with_errors(self, import_svc):
        data = {
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

        preview = import_svc.preview_from_dict(data)

        assert preview.errors
        with pytest.raises(ValueError, match="errors"):
            import_svc.commit_preview(preview)
        assert not import_svc._db.get_all_tests()

    def test_import_from_dict_preserves_explanation(self, import_svc):
        data = {
            "name": "Explained Test",
            "questions": [
                {
                    "text": "Q?",
                    "type": "multiple_choice",
                    "explanation": "Because A matches the rule.",
                    "options": [
                        {"text": "A", "correct": True},
                        {"text": "B", "correct": False},
                    ],
                }
            ],
        }
        test_id = import_svc.import_from_dict(data)
        db = import_svc._db
        question = db.get_questions_for_test(test_id)[0]
        assert question.explanation == "Because A matches the rule."

    def test_import_from_dict_preserves_newlines_and_markdown(self, import_svc):
        data = {
            "name": "Formatted Test",
            "questions": [
                {
                    "text": "First paragraph.\n\nSecond **bold** paragraph.",
                    "type": "multiple_choice",
                    "explanation": "Use <u>this rule</u>.\n\nThen apply it.",
                    "options": [
                        {"text": "Answer *one*", "correct": True},
                        {"text": "Answer two", "correct": False},
                    ],
                }
            ],
        }

        test_id = import_svc.import_from_dict(data)
        question = import_svc._db.get_questions_for_test(test_id)[0]

        assert question.text == "First paragraph.\n\nSecond **bold** paragraph."
        assert question.explanation == "Use <u>this rule</u>.\n\nThen apply it."
        assert question.options[0].text == "Answer *one*"

    def test_transactional_insert_rolls_back_on_option_failure(self, import_svc):
        from models.test import Test as TestModel

        test = TestModel(name="Rollback Test")
        questions = [
            Question(
                text="Q?",
                type="multiple_choice",
                correct_answer="A",
                options=[
                    QuestionOption(text="A", is_correct=True),
                    QuestionOption(text=object(), is_correct=False),
                ],
            )
        ]

        with pytest.raises(Exception):
            import_svc._db.create_test_with_questions(test, questions)

        assert not import_svc._db.get_all_tests()

    def test_commit_previews_calls_backup_service_for_bulk_import(self, import_svc):
        class FakeBackupService:
            def __init__(self):
                self.called = False

            def create_database_backup(self):
                self.called = True
                return None

        fake_backup = FakeBackupService()
        import_svc._backup_service = fake_backup
        data = {
            "name": "Bulk Preview",
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
        preview = import_svc.preview_from_dict(data)

        ids = import_svc.commit_previews([preview], create_backup=True)

        assert len(ids) == 1
        assert fake_backup.called is True

    def test_import_from_dict_uses_fallback_name(self, import_svc):
        data = {
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
        # No 'name' in payload; fallback must be used. Should not raise.
        test_id = import_svc.import_from_dict(data, fallback_name="Fallback")
        assert test_id > 0
        question = import_svc._db.get_questions_for_test(test_id)[0]
        assert question.explanation == ""

    def test_import_from_dict_rejects_missing_questions(self, import_svc):
        with pytest.raises(ValueError, match="questions"):
            import_svc.import_from_dict({"name": "Bad"})

    def test_import_essay_question(self, import_svc):
        data = {
            "name": "Essay Test",
            "questions": [
                {
                    "text": "Explain.",
                    "type": "essay",
                    "expected_answer": "The answer.",
                }
            ],
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            path = f.name

        try:
            test_id = import_svc.import_from_json(path)
            assert test_id > 0
        finally:
            os.unlink(path)


class TestTextImport:
    """Test plain-text import functionality."""

    def test_import_simple_text(self, import_svc):
        content = """1. What is 2+2?

a. 3
b. 4 -- correct
c. 5
d. 6

2. What color is the sky?

a. Red
b. Green
c. Blue -- correct
d. Yellow
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name

        try:
            test_id = import_svc.import_from_text(path, test_name="Text Test")
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_text_with_custom_name(self, import_svc):
        content = """1. Q?
a. A -- correct
b. B
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name

        try:
            test_id = import_svc.import_from_text(path, test_name="Custom Name")
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_text_with_already_established_marker(self, import_svc):
        content = """1. What standard?
a. Standard A
b. Standard B --already establishech
c. Standard C
d. Standard D -- correct
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name

        try:
            test_id = import_svc.import_from_text(path)
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_text_preserves_prompt_and_option_paragraphs(self, import_svc):
        content = """1. First prompt paragraph.

Second prompt paragraph with **bold** text.

a. First option paragraph.

Second option paragraph. -- correct
b. Other option
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(content)
            path = f.name

        try:
            test_id = import_svc.import_from_text(path, test_name="Paragraph Test")
            question = import_svc._db.get_questions_for_test(test_id)[0]
            assert (
                question.text == "First prompt paragraph.\n\n"
                "Second prompt paragraph with **bold** text."
            )
            assert (
                question.options[0].text
                == "First option paragraph.\n\nSecond option paragraph."
            )
        finally:
            os.unlink(path)

    def test_import_empty_file(self, import_svc):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            path = f.name

        try:
            with pytest.raises(ValueError, match="No questions"):
                import_svc.import_from_text(path)
        finally:
            os.unlink(path)

    def test_import_text_file_not_found(self, import_svc):
        with pytest.raises(FileNotFoundError):
            import_svc.import_from_text("/nonexistent/file.txt")

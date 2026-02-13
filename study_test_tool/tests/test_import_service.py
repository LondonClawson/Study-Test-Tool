"""Tests for ImportService."""

import json
import os
import tempfile

import pytest

from config.database import initialize_database
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

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = f.name

        try:
            test_id = import_svc.import_from_json(path)
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_json_missing_questions(self, import_svc):
        data = {"name": "Bad Test"}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = f.name

        try:
            with pytest.raises(ValueError, match="questions"):
                import_svc.import_from_json(path)
        finally:
            os.unlink(path)

    def test_import_json_empty_questions(self, import_svc):
        data = {"name": "Empty", "questions": []}

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
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

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
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
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
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
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
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
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write(content)
            path = f.name

        try:
            test_id = import_svc.import_from_text(path)
            assert test_id > 0
        finally:
            os.unlink(path)

    def test_import_empty_file(self, import_svc):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
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

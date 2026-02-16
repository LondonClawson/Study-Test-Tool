"""Tests for ExportService."""

import json
import os
import tempfile

import pytest

from config.database import initialize_database
from services.export_service import ExportService
from services.import_service import ImportService


@pytest.fixture
def db_path_for_export():
    """Temporary SQLite file for export tests."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    initialize_database(path)
    yield path
    os.unlink(path)


@pytest.fixture
def export_svc(db_path_for_export):
    """ExportService backed by a temporary database."""
    return ExportService(db_path_for_export)


@pytest.fixture
def import_svc(db_path_for_export):
    """ImportService sharing the same database as export_svc."""
    return ImportService(db_path_for_export)


@pytest.fixture
def sample_test_data():
    """Standard test data with MC and essay questions."""
    return {
        "name": "Export Test",
        "description": "A test for export testing",
        "questions": [
            {
                "text": "What is 1+1?",
                "type": "multiple_choice",
                "category": "Math",
                "options": [
                    {"text": "1", "correct": False},
                    {"text": "2", "correct": True},
                    {"text": "3", "correct": False},
                ],
            },
            {
                "text": "Explain gravity.",
                "type": "essay",
                "category": "Physics",
                "expected_answer": "Objects attract each other.",
            },
        ],
    }


@pytest.fixture
def imported_test_id(import_svc, sample_test_data):
    """Import the sample test and return its id."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as f:
        json.dump(sample_test_data, f)
        path = f.name

    try:
        return import_svc.import_from_json(path)
    finally:
        os.unlink(path)


class TestExportToJson:
    """Test JSON export functionality."""

    def test_export_creates_valid_json(self, export_svc, imported_test_id):
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        ) as f:
            path = f.name

        try:
            export_svc.export_to_json(imported_test_id, path)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert "name" in data
            assert "questions" in data
            assert isinstance(data["questions"], list)
        finally:
            os.unlink(path)

    def test_export_format_matches_import(
        self, export_svc, imported_test_id, sample_test_data
    ):
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        ) as f:
            path = f.name

        try:
            export_svc.export_to_json(imported_test_id, path)
            with open(path, "r", encoding="utf-8") as f:
                exported = json.load(f)

            assert exported["name"] == sample_test_data["name"]
            assert exported["description"] == sample_test_data["description"]
            assert len(exported["questions"]) == len(
                sample_test_data["questions"]
            )

            # Check MC question
            mc_q = exported["questions"][0]
            assert mc_q["type"] == "multiple_choice"
            assert mc_q["text"] == "What is 1+1?"
            assert len(mc_q["options"]) == 3
            correct_opts = [o for o in mc_q["options"] if o["correct"]]
            assert len(correct_opts) == 1
            assert correct_opts[0]["text"] == "2"

            # Check essay question
            essay_q = exported["questions"][1]
            assert essay_q["type"] == "essay"
            assert essay_q["expected_answer"] == "Objects attract each other."
        finally:
            os.unlink(path)

    def test_export_nonexistent_test_raises(self, export_svc):
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        ) as f:
            path = f.name

        try:
            with pytest.raises(ValueError, match="not found"):
                export_svc.export_to_json(99999, path)
        finally:
            os.unlink(path)

    def test_round_trip(
        self, export_svc, import_svc, imported_test_id, sample_test_data
    ):
        """Export then re-import produces an equivalent test."""
        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False
        ) as f:
            export_path = f.name

        try:
            export_svc.export_to_json(imported_test_id, export_path)
            new_test_id = import_svc.import_from_json(export_path)
            assert new_test_id != imported_test_id

            # Re-export the re-imported test and compare
            with tempfile.NamedTemporaryFile(
                suffix=".json", delete=False
            ) as f2:
                re_export_path = f2.name

            try:
                export_svc.export_to_json(new_test_id, re_export_path)
                with open(export_path, "r", encoding="utf-8") as f:
                    first_export = json.load(f)
                with open(re_export_path, "r", encoding="utf-8") as f:
                    second_export = json.load(f)
                assert first_export == second_export
            finally:
                os.unlink(re_export_path)
        finally:
            os.unlink(export_path)


class TestValidateTest:
    """Test export validation."""

    def test_validation_passes_complete_test(
        self, export_svc, imported_test_id
    ):
        warnings = export_svc.validate_test(imported_test_id)
        assert warnings == []

    def test_validation_catches_missing_mc_answer(
        self, db_path_for_export
    ):
        """MC question with no correct option triggers a warning."""
        svc = ImportService(db_path_for_export)
        data = {
            "name": "Bad MC",
            "questions": [
                {
                    "text": "Pick one",
                    "type": "multiple_choice",
                    "options": [
                        {"text": "A", "correct": False},
                        {"text": "B", "correct": False},
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
            test_id = svc.import_from_json(path)
        finally:
            os.unlink(path)

        export_svc = ExportService(db_path_for_export)
        warnings = export_svc.validate_test(test_id)
        assert len(warnings) == 1
        assert "Q1" in warnings[0]
        assert "no correct answer" in warnings[0]

    def test_validation_catches_missing_essay_answer(
        self, db_path_for_export
    ):
        """Essay question with no expected answer triggers a warning."""
        svc = ImportService(db_path_for_export)
        data = {
            "name": "Bad Essay",
            "questions": [
                {
                    "text": "Explain.",
                    "type": "essay",
                    "expected_answer": "",
                }
            ],
        }
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = f.name

        try:
            test_id = svc.import_from_json(path)
        finally:
            os.unlink(path)

        export_svc = ExportService(db_path_for_export)
        warnings = export_svc.validate_test(test_id)
        assert len(warnings) == 1
        assert "essay" in warnings[0].lower()

    def test_validation_nonexistent_test_raises(self, export_svc):
        with pytest.raises(ValueError, match="not found"):
            export_svc.validate_test(99999)

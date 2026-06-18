"""Import service for loading tests from JSON, text, and PDF files."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import QUESTION_TYPE_ESSAY, QUESTION_TYPE_MC
from database.db_manager import DatabaseManager
from models.question import Question, QuestionOption
from models.test import Test
from services import pdf_import_service
from services.backup_service import BackupService
from services.import_preview_service import ImportPreview, ImportPreviewService
from services.pdf_import_service import ConversionError


class ImportService:
    """Handles importing tests from JSON and plain-text files."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        self._db = DatabaseManager(db_path)
        self._backup_service = BackupService(db_path)
        self._preview_service = ImportPreviewService()

    # ── Preview / Commit ──────────────────────────────────────

    def preview_from_json(self, file_path: str) -> "ImportPreview":
        """Parse a JSON import file without writing it to the database."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.preview_from_dict(
            data, fallback_name=path.stem, source_name=path.name
        )

    def preview_from_dict(
        self,
        data: Dict,
        fallback_name: str = "",
        source_name: str = "",
    ) -> "ImportPreview":
        """Build an import preview from an already-parsed payload dict."""
        return self._preview_service.preview_from_dict(
            data,
            fallback_name=fallback_name,
            source_name=source_name,
        )

    def preview_from_text(
        self, file_path: str, test_name: Optional[str] = None
    ) -> "ImportPreview":
        """Parse a plain-text import file without writing it to the database."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")
        name = test_name if test_name else path.stem
        questions = self._parse_text_questions(content)
        if not questions:
            raise ValueError("No questions found in the text file.")

        payload = {
            "name": name,
            "description": f"Imported from {path.name}",
            "group_name": "",
            "questions": [
                self._preview_service.question_to_payload(question)
                for question in questions
            ],
        }
        return self.preview_from_dict(
            payload, fallback_name=name, source_name=path.name
        )

    def preview_from_pdf_pair(
        self, questions_pdf: str, answers_pdf: str
    ) -> "ImportPreview":
        """Parse a Questions/Answers PDF or DOCX pair without writing."""
        pair = pdf_import_service.build_pair_from_paths(
            Path(questions_pdf), Path(answers_pdf)
        )
        payload = pdf_import_service.convert_pair_to_dict(pair)
        return self.preview_from_dict(
            payload,
            fallback_name=pair.display_name,
            source_name=f"{pair.questions_pdf.name} + {pair.answers_pdf.name}",
        )

    def preview_from_pdf_folder(self, folder: str) -> List["ImportPreview"]:
        """Preview every discoverable PDF/DOCX pair in ``folder``."""
        root = Path(folder)
        if not root.is_dir():
            raise ConversionError(f"Not a directory: {folder}")

        pairs = pdf_import_service.discover_pairs(root)
        if not pairs:
            raise ConversionError(
                "No valid Questions/Answers PDF or DOCX pairs were found in this folder."
            )

        previews: List[ImportPreview] = []
        for pair in pairs:
            source_name = f"{pair.questions_pdf.name} + {pair.answers_pdf.name}"
            try:
                payload = pdf_import_service.convert_pair_to_dict(pair)
                previews.append(
                    self.preview_from_dict(
                        payload,
                        fallback_name=pair.display_name,
                        source_name=source_name,
                    )
                )
            except (ConversionError, ValueError) as exc:
                previews.append(
                    ImportPreview(
                        source_name=source_name,
                        test_name=pair.display_name,
                        description="",
                        group_name="",
                        question_count=0,
                        errors=[str(exc)],
                        payload=None,
                    )
                )
        return previews

    def commit_preview(
        self,
        preview: "ImportPreview",
        group_name_override: Optional[str] = None,
    ) -> int:
        """Persist a previously built import preview."""
        if preview.errors:
            raise ValueError("Cannot import a preview with errors.")
        if preview.payload is None:
            raise ValueError("Cannot import a preview without payload data.")

        payload = dict(preview.payload)
        if group_name_override is not None:
            payload["group_name"] = group_name_override.strip()

        test, questions = self._payload_to_models(
            payload, fallback_name=preview.test_name
        )
        return self._db.create_test_with_questions(test, questions)

    def commit_previews(
        self,
        previews: List["ImportPreview"],
        group_name_override: Optional[str] = None,
        create_backup: bool = False,
    ) -> List[int]:
        """Persist multiple previews, optionally backing up the database first."""
        importable = [preview for preview in previews if not preview.errors]
        if not importable:
            raise ValueError("No importable tests were found.")
        if create_backup:
            self.create_database_backup()
        return [
            self.commit_preview(preview, group_name_override=group_name_override)
            for preview in importable
        ]

    def create_database_backup(self) -> Optional[Path]:
        """Create a timestamped copy of the current SQLite database if it exists."""
        return self._backup_service.create_database_backup()

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

        return self.import_from_dict(data, fallback_name=path.stem)

    def import_from_dict(self, data: Dict, fallback_name: str = "") -> int:
        """Import a test from an already-parsed payload dict.

        Shared code path for JSON files and in-memory payloads produced by
        :mod:`services.pdf_import_service`.

        Args:
            data: Payload matching the import JSON contract.
            fallback_name: Used when the payload has no ``name`` field.

        Returns:
            The id of the created test.

        Raises:
            ValueError: If the payload format is invalid.
        """
        preview = self.preview_from_dict(data, fallback_name=fallback_name)
        return self.commit_preview(preview)

    # ── PDF Import ─────────────────────────────────────────────

    def import_from_pdf_pair(self, questions_pdf: str, answers_pdf: str) -> int:
        """Import a test from a Questions/Answers PDF or DOCX pair.

        PDF text is extracted with ``pdfminer.six`` (pure Python — no system
        binary needed); ``.docx`` files use ``python-docx``.

        Args:
            questions_pdf: Path to the Questions file (.pdf or .docx).
            answers_pdf: Path to the Answers file (.pdf or .docx).

        Returns:
            The id of the created test.

        Raises:
            ConversionError: If pairing fails or the files cannot be parsed
                into a valid payload (including scanned PDFs that contain no
                extractable text).
        """
        pair = pdf_import_service.build_pair_from_paths(
            Path(questions_pdf), Path(answers_pdf)
        )
        payload = pdf_import_service.convert_pair_to_dict(pair)
        return self.import_from_dict(payload, fallback_name=pair.display_name)

    def import_from_pdf_folder(self, folder: str) -> List[Dict[str, Any]]:
        """Import every discoverable PDF pair in ``folder``.

        Mirrors the standalone CLI's ``--batch`` mode: each pair is handled
        independently, errors are captured per-pair, and the returned list
        contains one report dict per pair (success, question_count on
        success; status='skipped' with an error message otherwise). Pairs
        that import successfully also include the created ``test_id``.

        Raises:
            ConversionError: If no pairs exist or the folder is missing.
        """
        root = Path(folder)
        if not root.is_dir():
            raise ConversionError(f"Not a directory: {folder}")

        pairs = pdf_import_service.discover_pairs(root)
        if not pairs:
            raise ConversionError(
                "No valid Questions/Answers PDF or DOCX pairs were found in this folder."
            )

        self.create_database_backup()

        results: List[Dict[str, Any]] = []
        for pair in pairs:
            base = {
                "pair": pair.display_name,
                "questions_pdf": str(pair.questions_pdf),
                "answers_pdf": str(pair.answers_pdf),
            }
            try:
                preview = self.preview_from_dict(
                    pdf_import_service.convert_pair_to_dict(pair),
                    fallback_name=pair.display_name,
                )
                test_id = self.commit_preview(preview)
                results.append(
                    {
                        **base,
                        "status": "success",
                        "test_id": test_id,
                        "question_count": preview.question_count,
                    }
                )
            except ConversionError as exc:
                results.append({**base, "status": "skipped", "error": str(exc)})
            except ValueError as exc:
                results.append({**base, "status": "skipped", "error": str(exc)})
        return results

    @staticmethod
    def _validate_json_format(data: Dict) -> None:
        """Validate the structure of imported JSON data."""
        ImportPreviewService.validate_json_format(data)

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
            explanation=q_data.get("explanation", "").strip(),
            options=options,
        )

    def _payload_to_models(
        self, payload: Dict, fallback_name: str = ""
    ) -> tuple[Test, List[Question]]:
        """Convert an import payload into model objects for transactional insert."""
        self._preview_service.validate_json_format(payload)
        errors, _ = self._preview_service.validate_payload_questions(payload)
        if errors:
            raise ValueError("; ".join(errors))

        test = Test(
            name=payload.get("name") or fallback_name,
            description=payload.get("description", ""),
            group_name=payload.get("group_name", ""),
        )
        questions = [
            self._parse_json_question(q_data, test_id=0)
            for q_data in payload.get("questions", [])
        ]
        return test, questions

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

        preview = self.preview_from_text(file_path, test_name=name)
        return self.commit_preview(preview)

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
        option_pattern = re.compile(r"^([a-dA-D])\s*[.)]\s*(.*?)$", re.MULTILINE)
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
            end = (
                option_matches[i + 1].start()
                if i + 1 < len(option_matches)
                else len(block)
            )
            raw_text = match.group(2) + block[start:end]

            raw_text = self._normalize_imported_text_block(raw_text)

            # Check for correct-answer marker
            is_correct, clean_text = self._extract_correct_marker(raw_text)

            # Handle garbled options (e.g., Q3 option b containing c's text)
            # If an option contains another option marker pattern mid-text,
            # truncate at that point
            next_option_in_text = re.search(r"\s+[☑]+\s+[A-Za-z]", clean_text)
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

    @staticmethod
    def _normalize_imported_text_block(text: str) -> str:
        """Fold soft-wrapped lines while preserving paragraph breaks."""
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        paragraphs = []
        current_lines = []

        for line in text.split("\n"):
            cleaned = re.sub(r"[ \t]+", " ", line).strip()
            if cleaned:
                current_lines.append(cleaned)
                continue
            if current_lines:
                paragraphs.append(" ".join(current_lines))
                current_lines = []

        if current_lines:
            paragraphs.append(" ".join(current_lines))

        return "\n\n".join(paragraphs).strip()

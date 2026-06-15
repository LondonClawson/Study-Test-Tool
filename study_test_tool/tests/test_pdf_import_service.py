"""Tests for the pure-Python parsing layer of pdf_import_service.

Most tests feed the parser cleaned text strings directly (the same shape
``extract_text_from_pdf`` + ``clean_text`` produce at runtime), so the suite
needs no real PDFs and runs on any machine.
"""

from pathlib import Path

import pytest

from services import pdf_import_service
from services.pdf_import_service import (
    ConversionError,
    PairSpec,
    build_payload,
    clean_text,
    convert_pair_to_dict,
    discover_pairs,
    find_partner_pdf,
    normalize_display_stem,
    pairing_key_from_stem,
    parse_answers,
    parse_questions,
    resolve_correct_letter,
    strip_role_suffix,
)


# ── Name normalization / pairing ───────────────────────────────────────────


class TestPairingKey:
    def test_collapses_multiple_choice_variants(self):
        assert pairing_key_from_stem("Week 1B Multiple Choice") == pairing_key_from_stem(
            "Week 1B Multiple-Choice"
        )

    def test_normalizes_whitespace(self):
        assert pairing_key_from_stem("  Week   3   Multiple-Choice ") == pairing_key_from_stem(
            "Week 3 Multiple Choice"
        )

    def test_display_stem_uses_hyphenated_form(self):
        assert normalize_display_stem("Week 1B Multiple Choice") == "Week 1B Multiple-Choice"

    def test_strip_role_suffix_questions(self):
        base, role = strip_role_suffix("Week 1B Multiple-Choice Questions")
        assert base == "Week 1B Multiple-Choice"
        assert role == "questions"

    def test_strip_role_suffix_answers_case_insensitive(self):
        base, role = strip_role_suffix("Week 2 MC ANSWERS")
        assert role == "answers"
        assert base == "Week 2 MC"

    def test_strip_role_suffix_rejects_bare_stem(self):
        with pytest.raises(ConversionError):
            strip_role_suffix("Week 1B Multiple-Choice")

    def test_pairing_key_is_whitespace_insensitive(self):
        """'Week 1B' and 'Week 1 B' must pair — instructors are inconsistent."""
        assert pairing_key_from_stem("Week 1B") == pairing_key_from_stem("Week 1 B")
        assert pairing_key_from_stem("Week1B") == pairing_key_from_stem("Week 1 B")


# ── Question parsing ───────────────────────────────────────────────────────


SAMPLE_QUESTIONS_TEXT = """1. What is 2+2?
A. 3
B. 4
C. 5
D. 6

2. What color is the sky?
(A) Red
(B) Green
(C) Blue
(D) Yellow
"""


class TestParseQuestions:
    def test_happy_path_with_dot_labels(self):
        questions = parse_questions(SAMPLE_QUESTIONS_TEXT)
        assert len(questions) == 2
        assert questions[0]["number"] == 1
        assert questions[0]["text"] == "What is 2+2?"
        assert [o["letter"] for o in questions[0]["options"]] == ["A", "B", "C", "D"]
        assert [o["text"] for o in questions[0]["options"]] == ["3", "4", "5", "6"]

    def test_accepts_parenthesized_labels(self):
        questions = parse_questions(SAMPLE_QUESTIONS_TEXT)
        assert questions[1]["options"][2]["text"] == "Blue"

    def test_multiline_option_is_folded(self):
        text = """1. Multi-line prompt
A. First line
   continuing here
B. Second
C. Third
D. Fourth
"""
        questions = parse_questions(text)
        assert questions[0]["options"][0]["text"] == "First line continuing here"

    def test_rejects_question_with_one_option(self):
        text = "1. Only one answer?\nA. Yes\n"
        with pytest.raises(ConversionError, match="answer choices"):
            parse_questions(text)

    def test_rejects_empty_text(self):
        with pytest.raises(ConversionError, match="No numbered questions"):
            parse_questions("")

    def test_skips_numbered_dot_in_flowing_text(self):
        """A line like '12.\\n' inside a scenario (e.g. wrapped 'May / 12.')
        is not a real question — it has zero option markers. The parser must
        skip such candidate blocks instead of failing the whole import."""
        text = (
            "11. Real question eleven\n"
            "A. yes\nB. no\n\n"
            "Some flowing text that ends with a date like May\n"
            "12.\n\n"
            "More flowing text inside a scenario.\n\n"
            "13. Real question thirteen\n"
            "A. yes\nB. no\n"
        )
        questions = parse_questions(text)
        # Q12 (the fake one) silently dropped; Q11 and Q13 kept.
        assert [q["number"] for q in questions] == [11, 13]

    def test_accepts_question_word_heading(self):
        text = """Question 1
What is 2+2?
A. 3
B. 4

Question 2:
What color is the sky?
A. Red
B. Blue
"""
        questions = parse_questions(text)
        assert [q["number"] for q in questions] == [1, 2]
        assert questions[0]["text"] == "What is 2+2?"


# ── Answer-key parsing ─────────────────────────────────────────────────────


class TestParseAnswers:
    def test_happy_path(self):
        answers = parse_answers("1. A\n2. B\n3. C\n")
        assert answers == {1: "A", 2: "B", 3: "C"}

    def test_rejects_empty(self):
        with pytest.raises(ConversionError, match="No answer key entries"):
            parse_answers("")

    def test_bare_letters_numbered_sequentially(self):
        """Week 2B-style answer key: bare letters → Q1, Q2, Q3, ..."""
        text = "C\nB\nC\nC\nA\nD\nA\nC\n"
        assert parse_answers(text) == {
            1: "C", 2: "B", 3: "C", 4: "C", 5: "A", 6: "D", 7: "A", 8: "C",
        }

    def test_na_skips_the_slot(self):
        """Week 1B-style: 'n/a' advances the implicit counter past Q8."""
        text = "D\nD\nB\nD\nB\nD\nC\nn/a\nA\nA\nB\nC\nC\nA\n"
        answers = parse_answers(text)
        assert 8 not in answers
        assert answers[7] == "C"
        assert answers[9] == "A"
        assert answers[14] == "A"
        assert len(answers) == 13

    def test_mixed_bare_then_numbered(self):
        """Week 2A-style: 8 bare letters, then explicit '29. B' and '32. C'."""
        text = " A\n A\n D\n D\nC\n A\n B\n A\n29. B\n32. C\n"
        answers = parse_answers(text)
        assert answers[1] == "A"
        assert answers[8] == "A"
        assert answers[29] == "B"
        assert answers[32] == "C"
        # Bare run is exactly 8 entries; no implicit numbers in Q9-Q28.
        assert set(answers.keys()) == {1, 2, 3, 4, 5, 6, 7, 8, 29, 32}

    def test_numbered_with_gaps_then_resumes_bare(self):
        """Week 4A-style: explicit '5. D' resets counter to 6 for next bare."""
        text = "1. C\n2. A\n3. C\n5. D\nA\nA\nD\n A\n10. B\n14. B\n15.\tD\n16. B\n"
        answers = parse_answers(text)
        assert answers == {
            1: "C", 2: "A", 3: "C", 5: "D",
            6: "A", 7: "A", 8: "D", 9: "A",
            10: "B", 14: "B", 15: "D", 16: "B",
        }

    def test_ignores_heading_and_separator_lines(self):
        """Title lines like 'PRACTICE MULTIPLE CHOICE ANSWER KEY' don't match."""
        text = (
            "Contracts I – Week 1-2\n\n"
            "PRACTICE MULTIPLE CHOICE ANSWER KEY\n\n"
            "D\nD\nB\n"
        )
        assert parse_answers(text) == {1: "D", 2: "D", 3: "B"}


# ── Correct-letter resolution ──────────────────────────────────────────────


class TestResolveCorrectLetter:
    def test_direct_match(self):
        assert resolve_correct_letter("B", ["A", "B", "C", "D"], 1) == "B"

    def test_efgh_remap(self):
        """Key uses A-D but the printed labels are E-H."""
        assert resolve_correct_letter("C", ["E", "F", "G", "H"], 1) == "G"

    def test_rejects_unknown_letter(self):
        with pytest.raises(ConversionError, match="does not match option labels"):
            resolve_correct_letter("Z", ["A", "B", "C", "D"], 7)


# ── Payload build ──────────────────────────────────────────────────────────


def _simple_questions():
    return [
        {
            "number": 1,
            "text": "Q1?",
            "options": [
                {"letter": "A", "text": "a1"},
                {"letter": "B", "text": "a2"},
            ],
        },
        {
            "number": 2,
            "text": "Q2?",
            "options": [
                {"letter": "A", "text": "b1"},
                {"letter": "B", "text": "b2"},
            ],
        },
    ]


class TestBuildPayload:
    def test_happy_path(self):
        payload = build_payload("Week 1", _simple_questions(), {1: "A", 2: "B"})
        assert payload["name"] == "Week 1"
        assert len(payload["questions"]) == 2
        # First question's correct is A -> a1.
        q1_opts = payload["questions"][0]["options"]
        assert q1_opts[0]["correct"] is True
        assert q1_opts[1]["correct"] is False

    def test_rejects_duplicate_question_numbers(self):
        dupe = _simple_questions()
        dupe[1]["number"] = 1
        with pytest.raises(ConversionError, match="Duplicate question numbers"):
            build_payload("Week 1", dupe, {1: "A", 2: "B"})

    def test_rejects_missing_answer(self):
        with pytest.raises(ConversionError, match="Missing answer"):
            build_payload("Week 1", _simple_questions(), {1: "A"})

    def test_silently_drops_extra_answer_key_entries(self):
        """Partial questions files are common (instructor uploaded a subset).

        An answer key with extras for Q3 (when only Q1, Q2 are listed) should
        not fail the import — just ignore the extras.
        """
        payload = build_payload(
            "Week 1", _simple_questions(), {1: "A", 2: "B", 3: "C"}
        )
        assert len(payload["questions"]) == 2


# ── clean_text ─────────────────────────────────────────────────────────────


class TestCleanText:
    def test_page_break_split_question_number(self):
        """A question number split across a page break should be stitched."""
        raw = "Some text\n1\n0. What is ten?\nA. ten\nB. eleven"
        cleaned = clean_text(raw)
        assert "10. What is ten?" in cleaned

    def test_unicode_line_separators_become_newlines(self):
        raw = "1. Q?\u2028A. Yes\u2029B. No\x85"
        cleaned = clean_text(raw)
        assert "1. Q?\nA. Yes\nB. No" in cleaned


# ── Bug regression: parse_answers accepts E–H ─────────────────────────────


class TestParseAnswersEFGH:
    def test_accepts_e_through_h_answer_letters(self):
        """Answer keys using E–H labels must not be silently dropped."""
        text = "1. E\n2. F\n3. G\n4. H\n"
        answers = parse_answers(text)
        assert answers == {1: "E", 2: "F", 3: "G", 4: "H"}

    def test_mixed_abcd_and_efgh(self):
        text = "1. A\n2. E\n3. C\n4. H\n"
        answers = parse_answers(text)
        assert answers == {1: "A", 2: "E", 3: "C", 4: "H"}


# ── Bug regression: discover_pairs and find_partner_pdf include .docx ──────


class TestDocxDiscovery:
    def test_discover_pairs_finds_docx_files(self, tmp_path):
        """discover_pairs must include .docx files, not just .pdf."""
        (tmp_path / "Week 1 Questions.docx").touch()
        (tmp_path / "Week 1 Answers.docx").touch()
        pairs = discover_pairs(tmp_path)
        assert len(pairs) == 1
        assert pairs[0].display_name == "Week 1"
        assert pairs[0].questions_pdf.suffix == ".docx"
        assert pairs[0].answers_pdf.suffix == ".docx"

    def test_discover_pairs_finds_mixed_pdf_docx(self, tmp_path):
        """discover_pairs must find a pair where one file is .pdf and the other .docx."""
        (tmp_path / "Week 2 Questions.pdf").touch()
        (tmp_path / "Week 2 Answers.docx").touch()
        pairs = discover_pairs(tmp_path)
        assert len(pairs) == 1

    def test_find_partner_pdf_finds_docx_partner(self, tmp_path):
        """find_partner_pdf must locate a .docx partner, not just .pdf."""
        q = tmp_path / "Week 3 Questions.docx"
        a = tmp_path / "Week 3 Answers.docx"
        q.touch()
        a.touch()
        partner = find_partner_pdf(q)
        assert partner == a


# ── Scanned-PDF detection ─────────────────────────────────────────────────


class TestScannedPdfDetection:
    """convert_pair_to_dict surfaces an actionable error for image-only PDFs."""

    def _make_pair(self, tmp_path: Path) -> PairSpec:
        q = tmp_path / "Week 9 Questions.pdf"
        a = tmp_path / "Week 9 Answers.pdf"
        q.touch()
        a.touch()
        return PairSpec(
            display_name="Week 9",
            pairing_key="week9",
            questions_pdf=q,
            answers_pdf=a,
            output_json=tmp_path / "Week 9.json",
        )

    def test_empty_questions_pdf_names_the_file(self, tmp_path, monkeypatch):
        pair = self._make_pair(tmp_path)
        monkeypatch.setattr(
            pdf_import_service, "_extract_file_text", lambda source: ""
        )
        with pytest.raises(ConversionError) as exc:
            convert_pair_to_dict(pair)
        assert "Week 9 Questions.pdf" in str(exc.value)
        assert "scanned image" in str(exc.value)

    def test_empty_answers_pdf_names_that_file(self, tmp_path, monkeypatch):
        pair = self._make_pair(tmp_path)
        # Real questions, empty answers — error must name the answers side.
        responses = {
            pair.questions_pdf: SAMPLE_QUESTIONS_TEXT,
            pair.answers_pdf: "\x0c\x0c\x0c",
        }
        monkeypatch.setattr(
            pdf_import_service,
            "_extract_file_text",
            lambda source: responses[source],
        )
        with pytest.raises(ConversionError) as exc:
            convert_pair_to_dict(pair)
        assert "Week 9 Answers.pdf" in str(exc.value)

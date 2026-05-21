"""Tests for the pure-Python parsing layer of pdf_import_service.

These tests never invoke ``pdftotext`` — they feed the parser the same kind
of cleaned text strings that ``extract_text`` + ``clean_text`` would produce
at runtime, so the suite runs on any machine without poppler installed.
"""

import pytest

from services.pdf_import_service import (
    ConversionError,
    build_payload,
    clean_text,
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


# ── Answer-key parsing ─────────────────────────────────────────────────────


class TestParseAnswers:
    def test_happy_path(self):
        answers = parse_answers("1. A\n2. B\n3. C\n")
        assert answers == {1: "A", 2: "B", 3: "C"}

    def test_rejects_empty(self):
        with pytest.raises(ConversionError, match="No numbered answer key"):
            parse_answers("")


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

    def test_rejects_extra_answer_key_entries(self):
        with pytest.raises(ConversionError, match="no matching question"):
            build_payload(
                "Week 1", _simple_questions(), {1: "A", 2: "B", 3: "C"}
            )


# ── clean_text ─────────────────────────────────────────────────────────────


class TestCleanText:
    def test_page_break_split_question_number(self):
        """A question number split across a page break should be stitched."""
        raw = "Some text\n1\n0. What is ten?\nA. ten\nB. eleven"
        cleaned = clean_text(raw)
        assert "10. What is ten?" in cleaned


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

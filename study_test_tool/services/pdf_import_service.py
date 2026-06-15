"""Convert paired Questions/Answers PDFs into Study-Test-Tool payloads.

This module contains the parsing engine used both by the in-app PDF import
path (via :class:`services.import_service.ImportService`) and by the
standalone ``convert_study_test_pdfs.py`` CLI shim at the repo root.

PDF text is extracted with ``pdfminer.six`` (pure Python — no system binary
required); ``.docx`` files use ``python-docx``. Scanned PDFs that have no
embedded text are detected and reported with an actionable error rather
than producing garbage downstream.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


DESCRIPTION = "Imported from Questions/Answers PDFs"
REPORT_NAME = "conversion_report.json"
OPTION_PREFIX_RE = r"^\s*\(?([A-H])\)?[.)]\s*"


class ConversionError(Exception):
    """Raised when a pair cannot be converted safely."""


@dataclass(frozen=True)
class PairSpec:
    """Resolved input/output paths for one Questions/Answers pair."""

    display_name: str
    pairing_key: str
    questions_pdf: Path
    answers_pdf: Path
    output_json: Path


# ── Name / pair resolution ──────────────────────────────────────────────────


def normalize_display_stem(stem: str) -> str:
    stem = stem.strip()
    stem = re.sub(r"\bMultiple\s+Choice\b", "Multiple-Choice", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem)
    return stem


def pairing_key_from_stem(stem: str) -> str:
    # Whitespace is stripped entirely so "Week 1B" and "Week 1 B" pair.
    normalized = normalize_display_stem(stem)
    normalized = normalized.lower().replace("-", "")
    normalized = re.sub(r"\s+", "", normalized)
    return normalized


def strip_role_suffix(stem: str) -> Tuple[str, str]:
    match = re.match(r"^(.*?)(?:\s+(Questions|Answers))$", stem, flags=re.IGNORECASE)
    if not match:
        raise ConversionError(f"Could not determine Questions/Answers role from '{stem}'.")
    return match.group(1).strip(), match.group(2).lower()


def build_pair_from_paths(questions_pdf: Path, answers_pdf: Path) -> PairSpec:
    if not questions_pdf.exists():
        raise ConversionError(f"Questions PDF not found: {questions_pdf}")
    if not answers_pdf.exists():
        raise ConversionError(f"Answers PDF not found: {answers_pdf}")

    q_base, q_role = strip_role_suffix(questions_pdf.stem)
    a_base, a_role = strip_role_suffix(answers_pdf.stem)
    if q_role != "questions":
        raise ConversionError(f"Questions file does not end with 'Questions': {questions_pdf.name}")
    if a_role != "answers":
        raise ConversionError(f"Answers file does not end with 'Answers': {answers_pdf.name}")

    q_key = pairing_key_from_stem(q_base)
    a_key = pairing_key_from_stem(a_base)
    if q_key != a_key:
        raise ConversionError(
            "Questions/Answers PDFs do not appear to be the same pair: "
            f"'{questions_pdf.name}' vs '{answers_pdf.name}'."
        )

    display_name = normalize_display_stem(q_base)
    parent = questions_pdf.parent
    return PairSpec(
        display_name=display_name,
        pairing_key=q_key,
        questions_pdf=questions_pdf,
        answers_pdf=answers_pdf,
        output_json=parent / f"{display_name}.json",
    )


def discover_pairs(root: Path) -> List[PairSpec]:
    grouped: Dict[str, Dict[str, Any]] = {}
    candidates = sorted(list(root.glob("*.pdf")) + list(root.glob("*.docx")))
    for pdf_path in candidates:
        try:
            base, role = strip_role_suffix(pdf_path.stem)
        except ConversionError:
            continue
        key = pairing_key_from_stem(base)
        bucket = grouped.setdefault(key, {"questions": None, "answers": None, "bases": []})
        bucket[role] = pdf_path
        bucket["bases"].append(base)

    pairs: List[PairSpec] = []
    for key in sorted(grouped):
        bucket = grouped[key]
        if bucket["questions"] and bucket["answers"]:
            pairs.append(build_pair_from_paths(bucket["questions"], bucket["answers"]))
    return pairs


def find_pair_by_stem(root: Path, stem: str) -> PairSpec:
    target_key = pairing_key_from_stem(stem)
    for pair in discover_pairs(root):
        if pair.pairing_key == target_key:
            return pair
    raise ConversionError(f"No Questions/Answers PDF pair found for stem '{stem}'.")


def find_partner_pdf(pdf_path: Path) -> Path:
    """Locate the partner PDF for ``pdf_path`` in the same directory.

    Given one half of a Questions/Answers pair, returns the matching other
    half by pairing key. Raises :class:`ConversionError` if no partner is
    found or the file name does not carry a Questions/Answers suffix.
    """
    base, role = strip_role_suffix(pdf_path.stem)
    target_key = pairing_key_from_stem(base)
    want_role = "answers" if role == "questions" else "questions"
    all_candidates = sorted(list(pdf_path.parent.glob("*.pdf")) + list(pdf_path.parent.glob("*.docx")))
    for candidate in all_candidates:
        if candidate == pdf_path:
            continue
        try:
            cand_base, cand_role = strip_role_suffix(candidate.stem)
        except ConversionError:
            continue
        if cand_role == want_role and pairing_key_from_stem(cand_base) == target_key:
            return candidate
    raise ConversionError(
        f"Could not locate the matching {want_role.capitalize()} PDF for '{pdf_path.name}'."
    )


# ── Text extraction ────────────────────────────────────────────────────────


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF using ``pdfminer.six`` (pure Python)."""
    from pdfminer.high_level import extract_text as _pdfminer_extract  # noqa: PLC0415

    return _pdfminer_extract(str(pdf_path))


def extract_text_from_docx(path: str) -> str:
    """Extract plain text from a .docx file."""
    from docx import Document  # noqa: PLC0415

    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def _extract_file_text(source: Path) -> str:
    if source.suffix.lower() == ".docx":
        return extract_text_from_docx(str(source))
    return extract_text_from_pdf(source)


# ── Text parsing ───────────────────────────────────────────────────────────


def clean_text(text: str) -> str:
    text = text.replace("\u2028", "\n").replace("\u2029", "\n").replace("\x85", "\n")
    text = text.replace("\f", "\n")
    text = re.sub(r"(?m)^\s*Torts\s*$", "", text)
    text = re.sub(
        r"(?m)^\s*Week .*Multiple(?:-|\s)Choice (Questions|Answers)\s*$",
        "",
        text,
    )
    # Garbled page-footer glyph runs (e.g. '! " # $ %&% 0% ()%*%') — these
    # come from a non-standard font that pdftotext/pdfminer can't decode and
    # otherwise leak into the last option's text.
    text = re.sub(
        r"""(?m)^[ \t]*!(?:[ \t]*[!"#$%&'()*+,\-./\d]){4,}[ \t]*$""",
        "",
        text,
    )
    text = re.sub(r"(?m)^\s*(\d)\s*\n\s*(\d\.)", r"\1\2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


_FACTS_HEADER_RE = re.compile(
    r"(?ms)^[ \t]*Facts for Questions?[ \t]+([^\n]+?)[ \t]*\n"
    r"(.*?)"
    r"(?=^[ \t]*Facts for Questions?[ \t]|^[ \t]*\d+\.[ \t]*$|^[ \t]*\d+\.[ \t]+\S|\Z)"
)


def _parse_question_number_list(s: str) -> List[int]:
    """Parse a Facts header's number list: '1' → [1]; '6-8' → [6,7,8]; '13 and 14' → [13,14]."""
    nums: List[int] = []
    s = s.replace("–", "-")
    for part in re.split(r"\s*(?:,|\band\b)\s*", s):
        part = part.strip()
        if not part:
            continue
        rng = re.match(r"(\d+)\s*-\s*(\d+)$", part)
        if rng:
            nums.extend(range(int(rng.group(1)), int(rng.group(2)) + 1))
            continue
        mm = re.search(r"\d+", part)
        if mm:
            nums.append(int(mm.group()))
    return nums


def _extract_scenarios(text: str) -> Tuple[str, Dict[int, str]]:
    """Pull 'Facts for Question(s) N' scenario blocks out of ``text``.

    Returns the text with the Facts blocks removed and a ``{question_num:
    scenario_text}`` map. The boundary for a scenario is the next Facts
    header or the next question-number marker at the start of a line. This
    lets ``parse_questions`` parse a clean stem+options chunk per question,
    and the caller can stitch the scenario back into the question's stem.
    """
    scenarios: Dict[int, str] = {}
    parts: List[str] = []
    last = 0
    for m in _FACTS_HEADER_RE.finditer(text):
        parts.append(text[last : m.start()])
        nums = _parse_question_number_list(m.group(1))
        scenario = " ".join(m.group(2).split())
        for n in nums:
            scenarios[n] = scenario
        last = m.end()
    parts.append(text[last:])
    return "".join(parts), scenarios


def parse_questions(text: str) -> List[Dict[str, Any]]:
    text, scenarios = _extract_scenarios(text)
    questions: List[Dict[str, Any]] = []
    question_marker = (
        r"(?:Question\s+(\d+)\s*[.):]?\s+|(\d+)\s*[.):]\s+)"
    )
    matches = re.finditer(
        rf"(?ims)^\s*{question_marker}(.*?)(?=^\s*{question_marker}|\Z)",
        text,
    )
    for match in matches:
        number = int(match.group(1) or match.group(2))
        body = match.group(3).strip()
        option_matches = list(re.finditer(rf"(?m){OPTION_PREFIX_RE}", body))
        # 0 option markers means this number-dot at line start is part of
        # flowing text (a wrapped date like "May / 12.\n" or a numbered list
        # inside a scenario), not a real question. Silently drop it — real
        # malformed questions will still surface as missing-answer errors
        # downstream.
        if not option_matches:
            continue
        if len(option_matches) < 2:
            raise ConversionError(f"Could not parse answer choices for question {number}.")

        stem = " ".join(body[: option_matches[0].start()].split())
        if not stem:
            raise ConversionError(f"Question {number} has empty prompt text.")

        options: List[Dict[str, str]] = []
        for index, option_match in enumerate(option_matches):
            letter = option_match.group(1)
            start = option_match.start()
            end = option_matches[index + 1].start() if index + 1 < len(option_matches) else len(body)
            chunk = body[start:end]
            chunk = re.sub(rf"(?m){OPTION_PREFIX_RE}", "", chunk, count=1)
            chunk = " ".join(chunk.split())
            if not chunk:
                raise ConversionError(f"Question {number} option {letter} is empty.")
            options.append({"letter": letter, "text": chunk})

        scenario = scenarios.get(number)
        if scenario:
            stem = f"{scenario}\n\n{stem}"
        questions.append({"number": number, "text": stem, "options": options})

    if not questions:
        raise ConversionError("No numbered questions were found in the Questions text.")
    return questions


_ANSWER_NUMBERED_RE = re.compile(r"^\s*(\d{1,3})\s*[.):]?\s*([A-H])\s*$")
_ANSWER_BARE_RE = re.compile(r"^\s*([A-H])\s*$")
_ANSWER_NA_RE = re.compile(r"^\s*n\s*/?\s*a\s*$", re.IGNORECASE)


def parse_answers(text: str) -> Dict[int, str]:
    """Parse an answer key, handling the variety of formats seen in the wild.

    Each non-empty line is classified:

    * ``"3. C"`` / ``"3) C"`` / ``"3 C"`` — explicit; records ``{3: "C"}`` and
      advances the implicit counter to ``4``.
    * ``"C"`` (a single A–H on its own line) — bare; records the next implicit
      slot and advances the counter.
    * ``"n/a"`` — skip the next implicit slot without recording an answer.
    * Anything else (headings, separators, blank lines) — ignored.

    The implicit counter starts at ``1`` so files that contain only bare
    letters are numbered sequentially. A ``ConversionError`` is raised only
    when zero answers were recorded — heading-only files still fail loudly.
    """
    answers: Dict[int, str] = {}
    next_implicit = 1

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        numbered = _ANSWER_NUMBERED_RE.match(line)
        if numbered:
            number = int(numbered.group(1))
            answers[number] = numbered.group(2)
            next_implicit = number + 1
            continue

        bare = _ANSWER_BARE_RE.match(line)
        if bare:
            answers[next_implicit] = bare.group(1)
            next_implicit += 1
            continue

        if _ANSWER_NA_RE.match(line):
            next_implicit += 1
            continue

    if not answers:
        raise ConversionError("No answer key entries were found in the Answers text.")
    return answers


def resolve_correct_letter(correct_letter: str, option_letters: List[str], number: int) -> str:
    """Resolve answer-key letters against printed option labels safely."""
    if correct_letter in option_letters:
        return correct_letter

    # Some source files print the four choices as E/F/G/H while the key still uses A-D.
    if option_letters == ["E", "F", "G", "H"] and correct_letter in {"A", "B", "C", "D"}:
        return option_letters[ord(correct_letter) - ord("A")]

    raise ConversionError(
        f"Question {number} answer key '{correct_letter}' does not match option labels {option_letters}."
    )


def build_payload(
    display_name: str,
    questions: List[Dict[str, Any]],
    answers: Dict[int, str],
) -> Dict[str, Any]:
    output_questions: List[Dict[str, Any]] = []
    parsed_numbers = [question["number"] for question in questions]
    if len(set(parsed_numbers)) != len(parsed_numbers):
        raise ConversionError("Duplicate question numbers found in the Questions text.")

    # Answer-key entries with no matching question are common when an
    # instructor uploads a partial questions file; silently drop them rather
    # than failing the whole import.
    answers = {n: letter for n, letter in answers.items() if n in set(parsed_numbers)}

    for question in questions:
        number = question["number"]
        correct_letter = answers.get(number)
        if not correct_letter:
            raise ConversionError(f"Missing answer for question {number}.")
        option_letters = [option["letter"] for option in question["options"]]
        resolved_letter = resolve_correct_letter(correct_letter, option_letters, number)

        options = [
            {"text": option["text"], "correct": option["letter"] == resolved_letter}
            for option in question["options"]
        ]
        if sum(1 for option in options if option["correct"]) != 1:
            raise ConversionError(f"Question {number} does not resolve to exactly one correct option.")

        output_questions.append(
            {
                "text": question["text"],
                "type": "multiple_choice",
                "options": options,
            }
        )

    return {
        "name": display_name,
        "description": DESCRIPTION,
        "questions": output_questions,
    }


# ── Pair conversion ────────────────────────────────────────────────────────


def _require_extractable_text(source: Path, text: str) -> None:
    """Raise an actionable error when a PDF/DOCX yielded no usable text.

    Scanned image PDFs come through as zero characters (or only form-feeds /
    whitespace). Bail out with a clear message pointing the user at OCR
    instead of letting the parser stumble forward on empty input.
    """
    if text.strip():
        return
    if source.suffix.lower() == ".docx":
        raise ConversionError(
            f"'{source.name}' contains no text. Confirm the file is not empty."
        )
    raise ConversionError(
        f"'{source.name}' has no extractable text — it appears to be a "
        "scanned image PDF. Open it in Word (File → Open will OCR it), save "
        "as .docx, and import that file instead."
    )


def convert_pair_to_dict(pair: PairSpec) -> Dict[str, Any]:
    """Extract + parse a Questions/Answers pair and return the import payload.

    Returns the in-memory payload dict; the GUI feeds this straight into
    :meth:`ImportService.import_from_dict`. Scanned PDFs (no embedded text)
    are detected up-front so the user gets an actionable error rather than a
    "No numbered questions found" puzzle.
    """
    question_raw = _extract_file_text(pair.questions_pdf)
    _require_extractable_text(pair.questions_pdf, question_raw)
    answer_raw = _extract_file_text(pair.answers_pdf)
    _require_extractable_text(pair.answers_pdf, answer_raw)

    questions = parse_questions(clean_text(question_raw))
    answers = parse_answers(clean_text(answer_raw))
    return build_payload(pair.display_name, questions, answers)


def convert_pair(pair: PairSpec) -> Dict[str, Any]:
    """Convert a pair and write a JSON file next to the PDFs.

    Returns a report-dict entry (success or skipped) matching the shape the
    standalone CLI has always produced. Safe — catches conversion errors and
    reports them instead of raising.
    """
    base_report = {
        "pair": pair.display_name,
        "questions_pdf": str(pair.questions_pdf),
        "answers_pdf": str(pair.answers_pdf),
        "output_json": str(pair.output_json),
    }
    try:
        payload = convert_pair_to_dict(pair)
        pair.output_json.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return {
            **base_report,
            "status": "success",
            "question_count": len(payload["questions"]),
        }
    except ConversionError as exc:
        return {
            **base_report,
            "status": "skipped",
            "error": str(exc),
        }


def build_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Bundle per-pair result dicts into the CLI-style report payload."""
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "processed": len(results),
        "succeeded": sum(1 for result in results if result["status"] == "success"),
        "skipped": sum(1 for result in results if result["status"] == "skipped"),
        "results": results,
    }

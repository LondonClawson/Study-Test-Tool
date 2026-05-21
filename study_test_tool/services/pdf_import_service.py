"""Convert paired Questions/Answers PDFs into Study-Test-Tool payloads.

This module contains the parsing engine used both by the in-app PDF import
path (via :class:`services.import_service.ImportService`) and by the
standalone ``convert_study_test_pdfs.py`` CLI shim at the repo root.

The engine shells out to ``pdftotext -layout`` (from poppler) to extract text
from PDFs, then parses the text into the import JSON shape the app already
accepts. No Python PDF dependency is introduced.
"""

from __future__ import annotations

import json
import re
import subprocess
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
    questions_txt: Path
    answers_txt: Path
    output_json: Path


# ── Name / pair resolution ──────────────────────────────────────────────────


def normalize_display_stem(stem: str) -> str:
    stem = stem.strip()
    stem = re.sub(r"\bMultiple\s+Choice\b", "Multiple-Choice", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem)
    return stem


def pairing_key_from_stem(stem: str) -> str:
    normalized = normalize_display_stem(stem)
    normalized = normalized.lower().replace("-", " ")
    normalized = re.sub(r"\s+", " ", normalized).strip()
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
        questions_txt=questions_pdf.with_suffix(".txt"),
        answers_txt=answers_pdf.with_suffix(".txt"),
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


# ── pdftotext boundary ─────────────────────────────────────────────────────


def require_pdftotext() -> None:
    """Raise :class:`ConversionError` with an actionable hint if missing."""
    try:
        subprocess.run(
            ["pdftotext", "-v"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ConversionError(
            "pdftotext is not installed. On macOS, run: brew install poppler"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise ConversionError(f"Unable to run pdftotext: {exc}") from exc


def extract_text(pdf_path: Path, txt_path: Path) -> None:
    subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), str(txt_path)],
        check=True,
        capture_output=True,
        text=True,
    )


def extract_text_from_docx(path: str) -> str:
    """Extract plain text from a .docx file."""
    from docx import Document  # noqa: PLC0415

    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def _extract_file_text(source: Path, txt_path: Path) -> str:
    if source.suffix.lower() == ".docx":
        return extract_text_from_docx(str(source))
    extract_text(source, txt_path)
    return txt_path.read_text(encoding="utf-8")


# ── Text parsing ───────────────────────────────────────────────────────────


def clean_text(text: str) -> str:
    text = text.replace("\f", "\n")
    text = re.sub(r"(?m)^\s*Torts\s*$", "", text)
    text = re.sub(
        r"(?m)^\s*Week .*Multiple(?:-|\s)Choice (Questions|Answers)\s*$",
        "",
        text,
    )
    text = re.sub(r"(?m)^\s*(\d)\s*\n\s*(\d\.)", r"\1\2", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_questions(text: str) -> List[Dict[str, Any]]:
    questions: List[Dict[str, Any]] = []
    matches = re.finditer(r"(?ms)^\s*(\d+)\.\s+(.*?)(?=^\s*\d+\.\s+|\Z)", text)
    for match in matches:
        number = int(match.group(1))
        body = match.group(2).strip()
        option_matches = list(re.finditer(rf"(?m){OPTION_PREFIX_RE}", body))
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

        questions.append({"number": number, "text": stem, "options": options})

    if not questions:
        raise ConversionError("No numbered questions were found in the Questions text.")
    return questions


def parse_answers(text: str) -> Dict[int, str]:
    answers = {int(num): letter for num, letter in re.findall(r"(?m)^\s*(\d+)\.\s*([A-H])\s*$", text)}
    if not answers:
        raise ConversionError("No numbered answer key entries were found in the Answers text.")
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

    extra_answers = sorted(set(answers) - set(parsed_numbers))
    if extra_answers:
        raise ConversionError(f"Answer key has entries with no matching question: {extra_answers}")

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


def convert_pair_to_dict(pair: PairSpec) -> Dict[str, Any]:
    """Run pdftotext + parse and return the import payload in memory.

    Writes ``.txt`` intermediates next to the PDFs (the CLI workflow keeps
    them for debugging), but does **not** write a JSON file. The caller is
    responsible for persistence — the GUI pipes the dict straight into
    :meth:`ImportService.import_from_dict`.
    """
    question_text = clean_text(_extract_file_text(pair.questions_pdf, pair.questions_txt))
    answer_text = clean_text(_extract_file_text(pair.answers_pdf, pair.answers_txt))

    questions = parse_questions(question_text)
    answers = parse_answers(answer_text)
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
        "questions_txt": str(pair.questions_txt),
        "answers_txt": str(pair.answers_txt),
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
    except subprocess.CalledProcessError as exc:
        return {
            **base_report,
            "status": "skipped",
            "error": f"pdftotext failed: {exc.stderr.strip() or exc}",
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

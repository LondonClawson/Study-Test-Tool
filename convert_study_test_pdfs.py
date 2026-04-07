#!/usr/bin/env python3
"""Convert paired Questions/Answers PDFs into Study-Test-Tool JSON."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert paired torts PDFs into Study-Test-Tool JSON."
    )
    parser.add_argument(
        "stem",
        nargs="?",
        help="Shared pair stem, such as 'Week 1B Multiple-Choice'.",
    )
    parser.add_argument(
        "--questions",
        help="Explicit path to the Questions PDF.",
    )
    parser.add_argument(
        "--answers",
        help="Explicit path to the Answers PDF.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all discoverable pairs in the working directory.",
    )
    parser.add_argument(
        "--report",
        help=f"Path for the JSON run report. Defaults to ./{REPORT_NAME}",
    )
    return parser.parse_args()


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


def strip_role_suffix(stem: str) -> tuple[str, str]:
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


def discover_pairs(root: Path) -> list[PairSpec]:
    grouped: dict[str, dict[str, Any]] = {}
    for pdf_path in sorted(root.glob("*.pdf")):
        try:
            base, role = strip_role_suffix(pdf_path.stem)
        except ConversionError:
            continue
        key = pairing_key_from_stem(base)
        bucket = grouped.setdefault(key, {"questions": None, "answers": None, "bases": []})
        bucket[role] = pdf_path
        bucket["bases"].append(base)

    pairs: list[PairSpec] = []
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


def require_pdftotext() -> None:
    try:
        subprocess.run(
            ["pdftotext", "-v"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ConversionError("pdftotext is not installed. Install poppler first.") from exc
    except subprocess.CalledProcessError as exc:
        raise ConversionError(f"Unable to run pdftotext: {exc}") from exc


def extract_text(pdf_path: Path, txt_path: Path) -> None:
    subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), str(txt_path)],
        check=True,
        capture_output=True,
        text=True,
    )


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


def parse_questions(text: str) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
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

        options: list[dict[str, str]] = []
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


def parse_answers(text: str) -> dict[int, str]:
    answers = {int(num): letter for num, letter in re.findall(r"(?m)^\s*(\d+)\.\s*([A-D])\s*$", text)}
    if not answers:
        raise ConversionError("No numbered answer key entries were found in the Answers text.")
    return answers


def resolve_correct_letter(correct_letter: str, option_letters: list[str], number: int) -> str:
    """Resolve answer-key letters against printed option labels safely."""
    if correct_letter in option_letters:
        return correct_letter

    # Some source files print the four choices as E/F/G/H while the key still uses A-D.
    if option_letters == ["E", "F", "G", "H"] and correct_letter in {"A", "B", "C", "D"}:
        return option_letters[ord(correct_letter) - ord("A")]

    raise ConversionError(
        f"Question {number} answer key '{correct_letter}' does not match option labels {option_letters}."
    )


def build_payload(display_name: str, questions: list[dict[str, Any]], answers: dict[int, str]) -> dict[str, Any]:
    output_questions: list[dict[str, Any]] = []
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


def convert_pair(pair: PairSpec) -> dict[str, Any]:
    try:
        extract_text(pair.questions_pdf, pair.questions_txt)
        extract_text(pair.answers_pdf, pair.answers_txt)

        question_text = clean_text(pair.questions_txt.read_text(encoding="utf-8"))
        answer_text = clean_text(pair.answers_txt.read_text(encoding="utf-8"))

        questions = parse_questions(question_text)
        answers = parse_answers(answer_text)
        payload = build_payload(pair.display_name, questions, answers)

        pair.output_json.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        return {
            "pair": pair.display_name,
            "status": "success",
            "questions_pdf": str(pair.questions_pdf),
            "answers_pdf": str(pair.answers_pdf),
            "questions_txt": str(pair.questions_txt),
            "answers_txt": str(pair.answers_txt),
            "output_json": str(pair.output_json),
            "question_count": len(payload["questions"]),
        }
    except subprocess.CalledProcessError as exc:
        return {
            "pair": pair.display_name,
            "status": "skipped",
            "questions_pdf": str(pair.questions_pdf),
            "answers_pdf": str(pair.answers_pdf),
            "questions_txt": str(pair.questions_txt),
            "answers_txt": str(pair.answers_txt),
            "output_json": str(pair.output_json),
            "error": f"pdftotext failed: {exc.stderr.strip() or exc}",
        }
    except ConversionError as exc:
        return {
            "pair": pair.display_name,
            "status": "skipped",
            "questions_pdf": str(pair.questions_pdf),
            "answers_pdf": str(pair.answers_pdf),
            "questions_txt": str(pair.questions_txt),
            "answers_txt": str(pair.answers_txt),
            "output_json": str(pair.output_json),
            "error": str(exc),
        }


def resolve_pairs(args: argparse.Namespace, root: Path) -> list[PairSpec]:
    if args.batch:
        pairs = discover_pairs(root)
        if not pairs:
            raise ConversionError("No valid Questions/Answers PDF pairs were found.")
        return pairs

    explicit_questions = bool(args.questions)
    explicit_answers = bool(args.answers)
    if explicit_questions or explicit_answers:
        if not (explicit_questions and explicit_answers):
            raise ConversionError("Use both --questions and --answers together.")
        return [build_pair_from_paths(Path(args.questions).expanduser(), Path(args.answers).expanduser())]

    if args.stem:
        return [find_pair_by_stem(root, args.stem)]

    raise ConversionError("Provide a pair stem, both --questions/--answers, or use --batch.")


def write_report(report_path: Path, results: list[dict[str, Any]]) -> None:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "processed": len(results),
        "succeeded": sum(1 for result in results if result["status"] == "success"),
        "skipped": sum(1 for result in results if result["status"] == "skipped"),
        "results": results,
    }
    report_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def print_summary(results: list[dict[str, Any]], report_path: Path) -> None:
    processed = len(results)
    succeeded = sum(1 for result in results if result["status"] == "success")
    skipped = sum(1 for result in results if result["status"] == "skipped")
    print(f"Processed: {processed} | Succeeded: {succeeded} | Skipped: {skipped}")
    for result in results:
        if result["status"] == "success":
            print(
                f"[OK] {result['pair']} -> {Path(result['output_json']).name} "
                f"({result['question_count']} questions)"
            )
        else:
            print(f"[SKIP] {result['pair']} -> {result['error']}")
    print(f"Report: {report_path}")


def main() -> int:
    args = parse_args()
    root = Path.cwd()
    report_path = Path(args.report).expanduser() if args.report else root / REPORT_NAME

    try:
        require_pdftotext()
        pairs = resolve_pairs(args, root)
    except ConversionError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    results = [convert_pair(pair) for pair in pairs]
    write_report(report_path, results)
    print_summary(results, report_path)
    return 1 if any(result["status"] == "skipped" for result in results) else 0


if __name__ == "__main__":
    sys.exit(main())

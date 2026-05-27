#!/usr/bin/env python3
"""Convert paired Questions/Answers PDFs into Study-Test-Tool JSON.

Thin CLI wrapper around ``study_test_tool.services.pdf_import_service``.
The parsing engine lives in the package so the in-app PDF import path and
this standalone CLI share one implementation. Usage is unchanged — see
``README-convert_study_test_pdfs.md``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# Make the package importable whether run from the repo root or elsewhere.
REPO_ROOT = Path(__file__).resolve().parent
PACKAGE_DIR = REPO_ROOT / "study_test_tool"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from services.pdf_import_service import (  # noqa: E402
    REPORT_NAME,
    ConversionError,
    build_pair_from_paths,
    build_report,
    convert_pair,
    discover_pairs,
    find_pair_by_stem,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert paired Questions/Answers PDFs into Study-Test-Tool JSON."
    )
    parser.add_argument(
        "stem",
        nargs="?",
        help="Shared pair stem, such as 'Week 1B Multiple-Choice'.",
    )
    parser.add_argument("--questions", help="Explicit path to the Questions PDF.")
    parser.add_argument("--answers", help="Explicit path to the Answers PDF.")
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


def resolve_pairs(args: argparse.Namespace, root: Path):
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
        return [
            build_pair_from_paths(
                Path(args.questions).expanduser(),
                Path(args.answers).expanduser(),
            )
        ]

    if args.stem:
        return [find_pair_by_stem(root, args.stem)]

    raise ConversionError("Provide a pair stem, both --questions/--answers, or use --batch.")


def write_report(report_path: Path, results: list[dict[str, Any]]) -> None:
    payload = build_report(results)
    report_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


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

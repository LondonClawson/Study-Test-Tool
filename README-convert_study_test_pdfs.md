# PDF Converter README

## Purpose

`convert_study_test_pdfs.py` converts paired `Questions.pdf` and `Answers.pdf` files into the JSON format expected by the installed Study-Test-Tool.

It was built and validated in:

- `/Users/aclaw/Downloads/Torts MC Practice`

The script does not read PDFs directly. It first uses `pdftotext -layout` to generate `.txt` intermediates, then parses those text files into Study-Test-Tool-compatible JSON.

## Requirements

- Python 3
- `pdftotext` from `poppler`

Install on macOS:

```bash
brew install poppler
```

Check installation:

```bash
pdftotext -v
```

## Expected Input Pattern

The script looks for matching PDF pairs such as:

- `Week 1B Multiple-Choice Questions.pdf`
- `Week 1B Multiple-Choice Answers.pdf`

It also tolerates minor naming variation such as:

- `Multiple Choice` vs `Multiple-Choice`

## Default Behavior

- Processes one pair at a time by default
- Keeps generated `.txt` intermediates
- Writes one app-native `.json` output per successful pair
- Writes a JSON report file summarizing successes and skips
- Skips ambiguous pairs instead of guessing

## Usage

Run one pair by shared stem:

```bash
python3 convert_study_test_pdfs.py "Week 1B Multiple-Choice"
```

Run one pair by explicit file paths:

```bash
python3 convert_study_test_pdfs.py \
  --questions "/path/to/Week 13B Multiple Choice Questions.pdf" \
  --answers "/path/to/Week 13B Multiple-Choice Answers.pdf"
```

Run all discoverable pairs in the current folder:

```bash
python3 convert_study_test_pdfs.py --batch
```

Write the report to a custom path:

```bash
python3 convert_study_test_pdfs.py "Week 1B Multiple-Choice" --report "/path/to/report.json"
```

## Outputs

For a successful pair, the script creates:

- `Questions.txt`
- `Answers.txt`
- `<shared stem>.json`

It also writes a run report such as:

- `conversion_report.json`

Each report entry includes:

- pair name
- status
- source PDF paths
- generated text paths
- output JSON path
- question count on success
- error message on skip

## Output JSON Shape

The JSON matches the current Study-Test-Tool import contract:

```json
{
  "name": "Week 1B Multiple-Choice",
  "description": "Imported from Questions/Answers PDFs",
  "questions": [
    {
      "text": "Question text",
      "type": "multiple_choice",
      "options": [
        { "text": "Option A", "correct": false },
        { "text": "Option B", "correct": true },
        { "text": "Option C", "correct": false },
        { "text": "Option D", "correct": false }
      ]
    }
  ]
}
```

## Parsing Rules

- Questions are parsed from numbered blocks like `1.`, `2.`, `3.`
- Options are parsed from labels such as `A.` or `(A)`
- Multi-line option text is folded into one line
- Answers are parsed from numbered key lines like `1. A`
- Matching is by question number, not just by position

## Safe-Failure Rules

The script skips a pair and reports an error if it finds:

- missing Questions or Answers PDFs
- unreadable extraction output
- no numbered questions
- no answer key
- missing answer for a question
- duplicate question numbers
- extra answer-key entries with no matching question
- answer choices that cannot be parsed safely
- no unique correct option

## Known Format Repairs

The script already handles these quirks:

- page-break splits like `1` on one line and `0.` on the next
- `Multiple Choice` / `Multiple-Choice` filename variation
- option labels written as `(A)` instead of `A.`
- a no-space option token such as `(D)Yes`
- four-choice sets printed as `E/F/G/H` when the answer key still uses `A/B/C/D`

## In-App Usage

The parsing engine now lives in `study_test_tool/services/pdf_import_service.py` and is wired into the GUI:

- **Import Test** button — pick any `.pdf` in a Questions/Answers pair. The tool auto-locates the matching half in the same folder by pairing key. If the partner cannot be found automatically, a second file dialog asks for it explicitly.
- **Import PDF Folder…** button — pick a directory; every discoverable pair is imported in one pass, and a summary dialog reports `N succeeded / M skipped` with per-pair error messages for anything that failed.

Both paths still require `pdftotext` (poppler). When it is missing, the GUI surfaces the `brew install poppler` hint instead of a stack trace.

`ImportService` exposes the new entry points if you need them programmatically:

- `import_from_pdf_pair(questions_pdf, answers_pdf) -> test_id`
- `import_from_pdf_folder(folder) -> list[report_dict]`
- `import_from_dict(data, fallback_name)` — the shared in-memory path used by both JSON and PDF imports.

## Integration Notes

This script at the repo root is now a thin CLI wrapper around `study_test_tool/services/pdf_import_service.py`. The standalone invocations documented above still work unchanged — the CLI shim just re-exports the same parsing and pairing functions the GUI calls.

Principles preserved:

1. `pdftotext` remains the boundary — no Python PDF library is added.
2. Skip-and-report behavior is unchanged: malformed pairs are reported, never guessed.
3. The JSON contract is unchanged; PDF and JSON imports share one code path inside `ImportService`.

## Validation History

This script has been validated locally against the installed Study-Test-Tool import service.

At the time of validation in this workspace:

- most weekly pairs converted successfully
- successful JSON outputs imported cleanly
- skipped pairs were explicitly reported instead of silently producing bad data

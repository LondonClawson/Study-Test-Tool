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

## Integration Notes

If you move this into the Study-Test-Tool repo later:

1. Keep it as a standalone utility first rather than wiring it into the GUI immediately.
2. Preserve the `pdftotext` requirement, since the workflow depends on text extraction first.
3. Keep the skip-and-report behavior. It is safer than auto-guessing on malformed materials.
4. If you later integrate it into the app, reuse the app’s existing JSON import path rather than inventing a second schema.

## Validation History

This script has been validated locally against the installed Study-Test-Tool import service.

At the time of validation in this workspace:

- most weekly pairs converted successfully
- successful JSON outputs imported cleanly
- skipped pairs were explicitly reported instead of silently producing bad data
